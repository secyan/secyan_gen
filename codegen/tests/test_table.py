import unittest

from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table


class TestTable(unittest.TestCase):
    def test_table_depth(self):
        table_a = Table(table_name="A", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ])

        table_b = Table(table_name="B", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ])

        table_c = Table(table_name="C", columns=[
            Column(name="e", column_type=TypeEnum.int),
            Column(name="f", column_type=TypeEnum.int)
        ])

        table_a.join(table_b, "a", "a")
        table_b.join(table_c, "e", "e")

        self.assertEqual(table_a.get_depth(), 0)
        self.assertEqual(table_b.get_depth(), 1)
        self.assertEqual(table_c.get_depth(), 2)
