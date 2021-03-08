import unittest

from sqlparse.sql import Identifier, Token

from codegen.node.SelectNode import SelectNode
from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table, CharacterEnum


class TestSelect(unittest.TestCase):
    def setUp(self) -> None:
        self.table_a = Table(table_name="A",
                             columns=[
                                 Column(name="a", column_type=TypeEnum.int),
                                 Column(name="b", column_type=TypeEnum.string)
                             ], owner=CharacterEnum.client)

    def assert_content_in_arr(self, arr, content: str):
        for a in arr:
            if content in a:
                self.assertTrue(True)
                return
        self.assertTrue(False)

    def test_simple_select(self):
        select_node = SelectNode(tables=[self.table_a])
        select_node.from_tables = [
            Identifier(tokens=[Token("int", "A")]),
        ]

        code = select_node.to_code()
        print(code)
        self.assert_content_in_arr(code, "Relation a(a_ri, a_ai);")
        self.assert_content_in_arr(code, "CLIENT")
        self.assert_content_in_arr(code, "{ Relation::INT,Relation::STRING }")

