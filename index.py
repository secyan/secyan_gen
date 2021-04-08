from os import getenv

import traceback
from flask import Flask, request, jsonify, Response

import json
from codegen.codegen import Parser
from codegen.codegen_fromDB import CodeGenDB
from codegen.database.postgresDB import PostgresDBPlan, PostgresDBDriver
from codegen.free_connex_codegen import FreeConnexParser
from codegen.table.free_connex_table import FreeConnexTable
from flask_cors import CORS

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
        parser = FreeConnexParser(sql=sql, tables=tables)
        output = parser.parse().to_output(data.get("functionName"))
        graph = parser.root_table.to_json(
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

        driver = PostgresDBDriver(password=password,
                                  user=user,
                                  database_name=database,
                                  host=host,
                                  port=port,
                                  tables=tables)

        parser = CodeGenDB(db_driver=driver, sql=sql, tables=tables)

        if "plan" in data and data["plan"] != "":
            plan = PostgresDBPlan.from_json(data["plan"], tables=tables)
            parser.parse(query_plan=plan)
        else:
            parser.parse()

        output = parser.to_output(function_name=data.get("functionName"))
        graph = parser.root_table.to_json(
            output_attrs=parser.get_output_attributes()) if parser.root_table else {}

        is_free_connex, error_tables = parser.is_free_connex()
        error_tables = [e.variable_table_name for e in error_tables]
        return jsonify(
            {"code": output, "joinGraph": graph, "isFreeConnex": is_free_connex, "errorTables": error_tables})

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
        driver.init(data=request.json['data'])
        return Response(status=201)
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=500)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
