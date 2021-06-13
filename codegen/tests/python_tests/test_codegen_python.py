import traceback
from typing import List

from secyan_python.constant import E_role
from secyan_python.utils import init_global_party

from .base_test import BaseTestCase
from ..data import SIMPLE_PLAN_SQL, simple_plan
from ..test_table_config import TEST_CONFIG
from ...codegen_python import CodeGenPython
from ...database.postgresDB import PostgresDBPlan, PostgresDBDriver
from ...table.python_free_connex_table import PythonFreeConnexTable
from multiprocessing import Queue, Process


def run_query(sql, role: E_role, queue: Queue, tables):
    try:
        init_global_party(address="0.0.0.0", port=7766, role=role)
        db_plan = PostgresDBPlan.from_json(simple_plan[0]['Plan'], tables=tables)
        db_driver = PostgresDBDriver(host="", database_name="", user="", password="", port="", tables=tables)
        codegen = CodeGenPython(sql=sql, db_driver=db_driver, tables=tables, annotation_name="q3_annot")
        codegen.parse(db_plan)
        results = codegen.to_output(limit_size=3)
        queue.put(results)
    except Exception:
        traceback.print_exc()
        queue.put("error")


class TestCodegenPython(BaseTestCase):

    def setUp(self) -> None:
        # noinspection PyTypeChecker
        self.tables: List[PythonFreeConnexTable] = [PythonFreeConnexTable.load_from_json(t) for t in TEST_CONFIG]
        self.replace_paths(mapping=self.generate_mapping())

    def test_select(self):
        client_queue = Queue()
        server_queue = Queue()

        client_p = Process(target=run_query, args=(SIMPLE_PLAN_SQL, E_role.CLIENT, client_queue, self.tables))
        server_p = Process(target=run_query, args=(SIMPLE_PLAN_SQL, E_role.SERVER, server_queue, self.tables))

        client_p.start()
        server_p.start()

        client_p.join()
        server_p.join()

        client_result = client_queue.get()
        server_result = server_queue.get()

        self.assertNotEqual(client_result, "error")
        self.assertNotEqual(server_result, "error")

        self.assertEqual(len(client_result), 0)
        self.assertEqual(len(server_result), 4)
