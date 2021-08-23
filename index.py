from os import getenv

import traceback
from flask import Flask, request, jsonify, Response
import json

from secyan_python.constant import E_role
from secyan_python.utils import init_global_party

from codegen.codegen import Parser
from codegen.codegen_fromDB import CodeGenDB
from codegen.codegen_python import CodeGenPython
from codegen.database.postgresDB import PostgresDBPlan, PostgresDBDriver
from codegen.free_connex_codegen import FreeConnexParser
from codegen.table.free_connex_table import FreeConnexTable
from flask_cors import CORS
from multiprocessing import Process, Queue

from codegen.table.python_free_connex_table import PythonFreeConnexTable
from codegen.utils.DataFetcher import DataFetcher
from codegen.utils.SchemaFetcher import SchemaFetcher

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return jsonify()


@app.route("/generate", methods=["POST"])
def generate_code():
    """
    Use default code gen
    :return:
    """
    try:
        data = request.json
        tables = [FreeConnexTable.load_from_json(t) for t in json.loads(data['table'])]
        sql = data['sql']
        annotation_name = data['annotation_name']
        parser = FreeConnexParser(sql=sql, tables=tables, annotation_name=annotation_name)
        output = parser.parse().to_output(data.get("functionName"))
        graph = parser.root_table.to_json_graph(
            output_attrs=parser.get_output_attributes())

        is_free_connex, error_tables = parser.is_free_connex()
        error_tables = [e.variable_table_name for e in error_tables]
        return jsonify(
            {"code": output, "joinGraph": graph, "isFreeConnex": is_free_connex, "errorTables": error_tables})
    except Exception as e:
        return Response(str(e), status=500)


@app.route("/generate_db", methods=["POST"])
def generate_code_by_db():
    """
    Perform a code generation by using db execution plan
    :return:
    """
    try:
        data: dict = request.json
        tables = [FreeConnexTable.load_from_json(t) for t in json.loads(data['table'])]

        sql = data['sql']
        password = getenv('password')
        user = getenv('user')
        database = data.get("database", None) if data.get("database", None) else getenv("database")
        host = getenv("host")
        port = getenv("port")
        annotation_name = data['annotation_name']

        driver = PostgresDBDriver(password=password,
                                  user=user,
                                  database_name=database,
                                  host=host,
                                  port=port,
                                  tables=tables)

        parser = CodeGenDB(db_driver=driver, sql=sql, tables=tables, annotation_name=annotation_name)

        if "plan" in data and data["plan"] != "":
            plan = PostgresDBPlan.from_json(data["plan"], tables=tables)
            parser.parse(query_plan=plan)
        else:
            parser.parse()

        output = parser.to_output(function_name=data.get("functionName"))
        graph = parser.root_table.to_json_graph(
            output_attrs=parser.get_output_attributes()) if parser.root_table else {}

        is_free_connex, error_tables = parser.is_free_connex()
        error_tables = [e.variable_table_name for e in error_tables]
        return jsonify(
            {"code": output, "joinGraph": graph, "isFreeConnex": is_free_connex, "errorTables": error_tables})

    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=500)


def run_query(sql, role: E_role, queue: Queue, tables, driver, annotation_name, num_of_rows):
    try:
        print("Starting connection")
        init_global_party(address="0.0.0.0", port=7766, role=role)
        parser = CodeGenPython(db_driver=driver, sql=sql, tables=tables, annotation_name=annotation_name)
        parser.parse()
        output = parser.to_output(limit_size=num_of_rows)
        graph = parser.root_table.to_json_graph(
            output_attrs=parser.get_output_attributes()) if parser.root_table else {}

        is_free_connex, error_tables = parser.is_free_connex()
        error_tables = [e.variable_table_name for e in error_tables]
        queue.put((False, output, graph, is_free_connex, error_tables))

    except Exception as e:
        queue.put((True, e))


@app.route("/generate_python", methods=["POST"])
def generate_python_result():
    """
    Perform a code generation and return the actual results
    :return:
    """
    try:

        data: dict = request.json
        tables = [PythonFreeConnexTable.load_from_json(t) for t in json.loads(data['table'])]

        sql = data['sql']
        password = getenv('password')
        user = getenv('user')
        database = data.get("database", None) if data.get("database", None) else getenv("database")
        host = getenv("host")
        port = getenv("port")
        annotation_name = data['annotation_name']
        num_of_rows = data.get("num_of_rows", 100)
        print("Generating python result")
        driver = PostgresDBDriver(password=password,
                                  user=user,
                                  database_name=database,
                                  host=host,
                                  port=port,
                                  tables=tables)

        client_queue = Queue()
        server_queue = Queue()

        client = Process(target=run_query,
                         args=(sql, E_role.CLIENT, client_queue, tables, driver, annotation_name, num_of_rows))

        server = Process(target=run_query,
                         args=(sql, E_role.SERVER, server_queue, tables, driver, annotation_name, num_of_rows))

        client.start()
        server.start()

        client.join()
        server.join()

        client_result = client_queue.get()
        server_result = server_queue.get()

        if client_result[0]:
            raise RuntimeError(client_result[1])

        if server_result[0]:
            raise RuntimeError(server_result[1])

        print(f"Client results: {len(client_result[1])}, server results: {len(server_result[1])}")

        return jsonify(
            {"client_result": client_result[1], "server_result": server_result[1], "joinGraph": client_result[2],
             "isFreeConnex": client_result[3], "errorTables": client_result[4]})

    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=500)


@app.route("/create_db", methods=["POST"])
def create_db():
    password = getenv('password')
    user = getenv('user')
    database = getenv("database")
    host = getenv("host")
    port = getenv("port")

    driver = PostgresDBDriver(password=password,
                              user=user,
                              database_name=database,
                              host=host,
                              port=port,
                              tables=[])
    try:
        driver.create_db_with_columns(data=request.json['data'])
        return Response(status=201)
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=500)


@app.route("/schema", methods=["GET"])
def get_table_schema():
    """
    Get tables' schema.
    :return:
    """
    password = getenv('password')
    user = getenv('user')
    database = getenv("database")
    host = getenv("host")
    port = getenv("port")

    driver = PostgresDBDriver(password=password,
                              user=user,
                              database_name=database,
                              host=host,
                              port=port,
                              tables=[])
    schema_fetcher = SchemaFetcher(db_driver=driver)
    try:
        tables = schema_fetcher.get_schema()
        return jsonify([t.to_json() for t in tables])
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=500)


@app.route("/download_data", methods=["POST"])
def get_data_with_annotation():
    password = getenv('password')
    user = getenv('user')
    database = getenv("database")
    host = getenv("host")
    port = getenv("port")
    output_dir = request.json.get("output_dir")

    driver = PostgresDBDriver(password=password,
                              user=user,
                              database_name=database,
                              host=host,
                              port=port,
                              tables=[])
    data_fetcher = DataFetcher(db_driver=driver)
    tables = [PythonFreeConnexTable.load_from_json(t) for t in json.loads(request.json.get("tables"))]

    try:
        tables = data_fetcher.store_data(output_dir=output_dir, tables=tables)
        return jsonify(
            [t.to_json() for t in tables]
        )
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=500)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", ssl_context="adhoc")
