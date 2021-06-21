import json
from multiprocessing import Process, Queue
from typing import Dict, List

from secyan_python.constant import E_role
from secyan_python.utils import init_global_party

from codegen.codegen_python import CodeGenPython
from codegen.database.postgresDB import PostgresDBPlan, PostgresDBDriver
from codegen.table.python_free_connex_table import PythonFreeConnexTable
import importlib.resources as pkg_resources
import codegen.tests.test_data as test_data
from codegen.tests.data import simple_plan, SIMPLE_PLAN_SQL
from codegen.tests.test_table_config import TEST_CONFIG


def replace_paths(tables, mapping: Dict[str, str]):
    for table in tables:
        if table.variable_table_name in mapping:
            replaced_name = mapping[table.variable_table_name]
            len_names = len(table.data_paths)
            table.data_paths = [replaced_name for i in range(len_names)]


def generate_mapping() -> Dict[str, str]:
    mapping = {}

    with pkg_resources.path(test_data, "customer.tbl") as p:
        mapping['customer'] = str(p)

    with pkg_resources.path(test_data, "lineitem.tbl") as p:
        mapping['lineitem'] = str(p)

    with pkg_resources.path(test_data, "orders.tbl") as p:
        mapping['orders'] = str(p)

    with pkg_resources.path(test_data, "part.tbl") as p:
        mapping['part'] = str(p)

    with pkg_resources.path(test_data, "partsupp.tbl") as p:
        mapping['partsupp'] = str(p)

    with pkg_resources.path(test_data, "supplier.tbl") as p:
        mapping['supplier'] = str(p)

    return mapping


def run_query(sql, role: E_role, queue: Queue, tables):
    init_global_party(address="0.0.0.0", port=7766, role=role)
    db_plan = PostgresDBPlan.from_json(simple_plan[0]['Plan'], tables=tables)
    db_driver = PostgresDBDriver(host="", database_name="", user="", password="", port="", tables=tables)
    codegen = CodeGenPython(sql=sql, db_driver=db_driver, tables=tables, annotation_name="q3_annot")
    codegen.parse(db_plan)
    results = codegen.to_output(output_table_name="orders", limit_size=3)
    queue.put(results)


if __name__ == '__main__':
    tables: List[PythonFreeConnexTable] = [PythonFreeConnexTable.load_from_json(t) for t in TEST_CONFIG]
    replace_paths(mapping=generate_mapping(), tables=tables)
    # j = json.dumps([t.to_json() for t in tables])
    client_queue = Queue()
    server_queue = Queue()

    client_p = Process(target=run_query, args=(SIMPLE_PLAN_SQL, E_role.CLIENT, client_queue, tables))
    server_p = Process(target=run_query, args=(SIMPLE_PLAN_SQL, E_role.SERVER, server_queue, tables))

    client_p.start()
    server_p.start()

    client_p.join()
    server_p.join()

    client_result = client_queue.get()
    server_result = server_queue.get()

    print(client_result)
    print(server_result)
