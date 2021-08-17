import unittest

from codegen.free_connex_codegen import FreeConnexParser
from codegen.node.cpp_nodes import SelectNode
from codegen.table import Table, Column, TypeEnum, CharacterEnum, FreeConnexTable
from codegen.tests.test_table_config import TEST_CONFIG


class AggregationFunctionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]


    def test_max(self):
        query = """
                    select max(o_shippriority) from orders;
                 """
        codegen = FreeConnexParser(tables=self.tables, sql=query, annotation_name="demo")

        self.assertTrue(len(self.tables) > 0)
        codegen.parse()
        # Find select node
        select_node: SelectNode = codegen.root.next
        self.assertEqual(select_node.used_aggregation_function, "max")


    def test_sum(self):
        query = """
                    select sum(o_shippriority) from orders;
                 """
        codegen = FreeConnexParser(tables=self.tables, sql=query, annotation_name="demo")

        self.assertTrue(len(self.tables) > 0)
        codegen.parse()
        # Find select node
        select_node: SelectNode = codegen.root.next
        self.assertEqual(select_node.used_aggregation_function, "sum")
