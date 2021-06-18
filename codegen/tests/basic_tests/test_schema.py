from typing import List, Tuple
from unittest import TestCase

from codegen.database.baseDB import DatabaseDriver
from codegen.database.dbplan import DBPlan
from codegen.table import TypeEnum
from codegen.utils.SchemaFetcher import SchemaFetcher


class MockDatabaseDriver(DatabaseDriver):
    def __init__(self):
        super().__init__([])

    def get_query_plan(self, sql: str) -> DBPlan:
        pass

    def execute(self, sql: str) -> List[Tuple]:
        return [
            ('supplier', 's_suppkey', 'integer'),
            ('supplier', 's_name', 'text'),
            ('customer', 'c_name', 'text'),
            ('customer', 'c_address', 'text'),
            ('lineitem', 'l_discount', 'real'),
            ('orders', 'o_shippriority', 'integer'),
            ('orders', 'o_comment', 'text'),
        ]


class TestSchemaFetcher(TestCase):
    def setUp(self):
        self.driver = MockDatabaseDriver()

    def test_schema(self):
        schema_fetcher = SchemaFetcher(db_driver=self.driver)
        data = schema_fetcher.get_schema()
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0].variable_table_name, "supplier")
        self.assertEqual(data[0].original_column_names[0].column_type, TypeEnum.int)

        self.assertEqual(data[1].variable_table_name, "customer")
        self.assertEqual(data[1].original_column_names[0].column_type, TypeEnum.string)

        self.assertEqual(data[2].variable_table_name, "lineitem")
        self.assertEqual(data[2].original_column_names[0].column_type, TypeEnum.decimal)

        self.assertEqual(data[3].variable_table_name, "orders")
        self.assertEqual(data[3].original_column_names[0].column_type, TypeEnum.int)
