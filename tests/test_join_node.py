import unittest

from sqlparse.sql import Identifier, Token

from codegen.node.JoinNode import JoinData, JoinNode
from codegen.node.SelectNode import SelectNode
from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table


class JoinNodeTest(unittest.TestCase):
    def test_simple_join1(self):
        data = [JoinData(left="aa", right="ba")]
        table_a = Table(table_name="A",
                        columns=[Column(name="aa", column_type=TypeEnum.int),
                                 Column(name="b", column_type=TypeEnum.int),
                                 Column(name="c", column_type=TypeEnum.int)])

        table_b = Table(table_name="B",
                        columns=[Column(name="ba", column_type=TypeEnum.int),
                                 Column(name="e", column_type=TypeEnum.int)])

        root = SelectNode(tables=[table_a, table_b])
        root.identifier_list = [Identifier(tokens=[Token(None, "b")]), Identifier(tokens=[Token(None, "c")])]

        root.next = JoinNode(join_list=data, tables=[table_a, table_b])
        root.next.prev = root

        result = root.next.to_code()
        print(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'b.Aggregate({ "ba" })\na.SemiJoin(b,"aa" , "ba");')

    def test_simple_join2(self):
        data = [JoinData(left="aa", right="ab"), JoinData(left="ec", right="eb")]
        table_a = Table(table_name="A",
                        columns=[Column(name="aa", column_type=TypeEnum.int),
                                 Column(name="b", column_type=TypeEnum.int),
                                 Column(name="c", column_type=TypeEnum.int)])

        table_b = Table(table_name="B",
                        columns=[Column(name="ab", column_type=TypeEnum.int),
                                 Column(name="eb", column_type=TypeEnum.int)])

        table_c = Table(table_name="C",
                        columns=[Column(name="ec", column_type=TypeEnum.int),
                                 Column(name="f", column_type=TypeEnum.int)])

        tables = [table_a, table_b, table_c]

        root = SelectNode(tables=tables)
        root.identifier_list = [Identifier(tokens=[Token(None, "ec")]), Identifier(tokens=[Token(None, "f")])]

        root.next = JoinNode(join_list=data, tables=tables)
        root.next.prev = root

        result = root.next.to_code()
        print(result)
        self.assertEqual(len(result), 3)
        # self.assertEqual(result[0], 'a.SemiJoin(b,"aa" , "ba");\na.Aggregate("b","c")')
