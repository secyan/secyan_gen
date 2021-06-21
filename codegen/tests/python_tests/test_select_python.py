from unittest import TestCase

from sqlparse.sql import Identifier, Token

from codegen.node.python_nodes import SelectNodePython
from codegen.table import FreeConnexTable, Table, Column, TypeEnum
from codegen.table.python_free_connex_table import PythonFreeConnexTable
from codegen.table.table import CharacterEnum
from codegen.tests.test_table_config import TEST_CONFIG


class TestSelectPython(TestCase):

    # def setUp(self) -> None:
    #     self.tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]

    def test_select(self):
        table_a = PythonFreeConnexTable(table_name="A",
                                        columns=[
                                            Column(name="a", column_type=TypeEnum.int),
                                            Column(name="b", column_type=TypeEnum.string)
                                        ], owner=CharacterEnum.client, data_sizes=[100], data_paths=[""],
                                        annotations=[])

        node = SelectNodePython(tables=[table_a], annotation_name="demo")
        node.from_tables = [
            Identifier(tokens=[Token("int", "A")]),
        ]
        relations = node.to_code(table_a.get_root(), should_load_data=False)
        self.assertEqual(len(relations), 1)

        table = relations[0]
        self.assertEqual(table.variable_table_name, "a")
        self.assertIsNotNone(table.relation)

    def test_select2(self):
        table_a = PythonFreeConnexTable(table_name="A",
                                        columns=[
                                            Column(name="a", column_type=TypeEnum.int),
                                            Column(name="b", column_type=TypeEnum.string)
                                        ], owner=CharacterEnum.client, data_sizes=[100], data_paths=[""],
                                        annotations=[])

        table_b = PythonFreeConnexTable(table_name="B",
                                        columns=[
                                            Column(name="c", column_type=TypeEnum.int),
                                            Column(name="d", column_type=TypeEnum.string)
                                        ], owner=CharacterEnum.server, data_sizes=[100], data_paths=[""],
                                        annotations=[])

        node = SelectNodePython(tables=[table_a, table_b], annotation_name="demo")
        node.from_tables = [
            Identifier(tokens=[Token("int", "A")]),
            Identifier(tokens=[Token("int", "B")]),
        ]
        relations = node.to_code(table_a.get_root(), should_load_data=False)
        self.assertEqual(len(relations), 2)

        table = relations[0]
        self.assertEqual(table.variable_table_name, "a")
        self.assertIsNotNone(table.relation)

        table = relations[1]
        self.assertEqual(table.variable_table_name, "b")
        self.assertIsNotNone(table.relation)
