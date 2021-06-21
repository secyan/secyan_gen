import unittest
from typing import List, Callable, Tuple
from codegen.table import FreeConnexTable
from codegen.database import DBPlan
from codegen.database.postgresDB import PostgresDBPlan
from codegen.table.table import Table
from codegen.tests.test_table_config import TEST_CONFIG, TEST_DB_PLAN
from codegen.database.baseDB import DatabaseDriver
from codegen.codegen_fromDB import CodeGenDB, DBPlan


class MockDB(DatabaseDriver):
    def get_query_plan(self, sql: str) -> DBPlan:
        return PostgresDBPlan.from_json(TEST_DB_PLAN[0]["Plan"], tables=self.tables)

    def execute(self, sql: str) -> List[Tuple]:
        pass

    def execute_save(self, sql: str, output_filename: str):
        pass


class TestCodegenDB(unittest.TestCase):

    def is_free_connex_table(self):
        return True, []

    def test_join(self):
        tables = [Table.load_from_json(t) for t in TEST_CONFIG]
        plan = PostgresDBPlan.from_json(TEST_DB_PLAN[0]["Plan"], tables=tables)
        plan.perform_join(is_free_connex_table=self.is_free_connex_table)

        order_table = list(filter(lambda t: t.variable_table_name == "orders", tables))[0]
        lineitem_table = list(filter(lambda t: t.variable_table_name == "lineitem", tables))[0]
        customer_table = list(filter(lambda t: t.variable_table_name == "customer", tables))[0]

        # self.assertEqual(order_table.parent, lineitem_table)
        # self.assertEqual(lineitem_table.parent, customer_table)
        # self.assertEqual(customer_table.parent, None)

    def test_select(self):
        tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]
        sql = "select l_orderkey from LINEITEM, CUSTOMER, ORDERS"
        driver = MockDB(tables=tables)
        parser = CodeGenDB(sql=sql, db_driver=driver, tables=tables, annotation_name="")
        parser.parse()

