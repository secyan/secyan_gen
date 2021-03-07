import unittest

from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table


class JoinTest(unittest.TestCase):
    def setUp(self):
        self.a_table = Table(table_name="a",
                             columns=[Column(name="name", column_type=TypeEnum.string),
                                      Column(name="id", column_type=TypeEnum.int)])
        self.b_table = Table(table_name="b", columns=[Column(name="name", column_type=TypeEnum.string),
                                                      Column(name="id", column_type=TypeEnum.int)])

        self.c_table = Table(table_name="c", columns=[
            Column(name="name", column_type=TypeEnum.string),
            Column(name="id", column_type=TypeEnum.int),
            Column(name="address", column_type=TypeEnum.string)
        ])

    def test_simple_join(self):
        self.a_table.join(self.b_table, "id", "id")
        self.assertEqual(len(self.a_table.children), 1)
        column_names = self.a_table.column_names
        self.assertEqual(len(column_names), 3)

    def test_simple_join_2(self):
        self.b_table.join(self.c_table, "id", "id")
        column_names = self.b_table.column_names
        self.assertEqual(len(column_names), 4)
        expected_names = ["c.name", "b.id", "c.address", "b.name"]
        for c in column_names:
            self.assertTrue(c.name_with_table in expected_names)
