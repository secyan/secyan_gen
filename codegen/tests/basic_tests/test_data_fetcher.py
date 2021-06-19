from typing import List, Tuple
from unittest import TestCase

from codegen.database.baseDB import DatabaseDriver
from codegen.database.dbplan import DBPlan
from codegen.table import TypeEnum
from codegen.utils.DataFetcher import DataFetcher
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


class TestDataFetcher(TestCase):
    def setUp(self):
        self.driver = MockDatabaseDriver()

    def test_simple_fetcher(self):
        schema_fetcher = SchemaFetcher(db_driver=self.driver)
        data = schema_fetcher.get_schema()
        data_fetcher = DataFetcher(db_driver=self.driver)
        new_tables = data_fetcher.store_data(output_dir="/test", tables=data, should_write=False)
        self.assertEqual(len(new_tables), 4)
        self.assertEqual(new_tables[0].data_sizes, [0])
        self.assertEqual(new_tables[0].data_paths, ['/test/supplier.tbl'])

        self.assertEqual(new_tables[3].data_sizes, [0])
        self.assertEqual(new_tables[3].data_paths, ['/test/orders.tbl'])
