from unittest import TestCase

from codegen.codegen_fromDB import CodeGenDB
from codegen.database.postgresDB import PostgresDBDriver, PostgresDBPlan
from codegen.table import FreeConnexTable
from codegen.tests.data import simple_plan, SIMPLE_PLAN_SQL
from codegen.tests.test_table_config import TEST_CONFIG


class TestQueryPlanJoin(TestCase):

    def setUp(self) -> None:
        self.tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]

    def test_simple_join(self):
        db_plan = PostgresDBPlan.from_json(simple_plan[0]['Plan'], tables=self.tables)
        db_driver = PostgresDBDriver(host="", database_name="", user="", password="", port="", tables=self.tables)
        codegen = CodeGenDB(sql=SIMPLE_PLAN_SQL, db_driver=db_driver, tables=self.tables, annotation_name="demo")
        codegen.parse(query_plan=db_plan)
        codegen.to_output()
        root = codegen.root_table
        self.assertEqual("orders", root.variable_table_name)
        self.assertTrue(codegen.is_free_connex())
