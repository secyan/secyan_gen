import unittest
from codegen.database.postgresDB import PostgresDBPlan, PostgresDBDriver
from codegen.table.table import Table
from codegen.tests.test_table_config import TEST_CONFIG, TEST_DB_PLAN


class TestCodegenDB(unittest.TestCase):

    def test_join(self):
        tables = [Table.load_from_json(t) for t in TEST_CONFIG]
        plan = PostgresDBPlan.from_json(TEST_DB_PLAN[0]["Plan"], tables=tables)
        plan.perform_join()

        order_table = list(filter(lambda t: t.variable_table_name == "orders", tables))[0]
        lineitem_table = list(filter(lambda t: t.variable_table_name == "lineitem", tables))[0]
        customer_table = list(filter(lambda t: t.variable_table_name == "customer", tables))[0]

        self.assertEqual(order_table.parent, lineitem_table)
        self.assertEqual(lineitem_table.parent, customer_table)
        self.assertEqual(customer_table.parent, None)

