import unittest

import sqlparse
from sqlparse.sql import Identifier, Token

from codegen.node.SelectNode import SelectNode
from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table, CharacterEnum
from codegen.tests.base_test_case import QueryTestCase


class TestSelect(QueryTestCase):
    def setUp(self) -> None:
        self.table_a = Table(table_name="A",
                             columns=[
                                 Column(name="a", column_type=TypeEnum.int),
                                 Column(name="b", column_type=TypeEnum.string)
                             ], owner=CharacterEnum.client, data_sizes=[100])

    def test_simple_select(self):
        select_node = SelectNode(tables=[self.table_a])
        select_node.from_tables = [
            Identifier(tokens=[Token("int", "A")]),
        ]

        code = select_node.to_code(self.table_a.get_root())
        print(code)
        self.assert_content_in_arr(code, "Relation a(a_ri, a_ai);")
        self.assert_content_in_arr(code, "CLIENT")
        self.assert_content_in_arr(code, "{ Relation::INT,Relation::STRING }")

    def test_select_with_aggregation(self):
        sql = """select sum(a) from A"""
        tokens = sqlparse.parse(sql)[0].tokens
        select_node = SelectNode(tables=[self.table_a])

        select_node.from_tables = tokens[6]
        select_node.set_identifier_list([tokens[2]])
        select_node.merge()
        self.assertFalse(select_node.tables[0].is_bool)

    def test_select_with_aggregation2(self):
        sql = """select sum(a) as re from A"""
        tokens = sqlparse.parse(sql)[0].tokens
        select_node = SelectNode(tables=[self.table_a])

        select_node.from_tables = tokens[6]
        select_node.set_identifier_list([tokens[2]])
        select_node.merge()
        self.assertFalse(select_node.tables[0].is_bool)