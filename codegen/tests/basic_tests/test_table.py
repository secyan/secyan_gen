import unittest

from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table


class TestTable(unittest.TestCase):
    def test_table_height(self):
        """
        A - B -C
        """
        table_a = Table(table_name="A", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ], data_sizes=[100], data_paths=[""], annotations=[])

        table_b = Table(table_name="B", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ], data_sizes=[100], data_paths=[""], annotations=[])

        table_c = Table(table_name="C", columns=[
            Column(name="e", column_type=TypeEnum.int),
            Column(name="f", column_type=TypeEnum.int)
        ], data_sizes=[100], data_paths=[""], annotations=[])

        table_a.join(table_b, "a", "a")
        table_b.join(table_c, "e", "e")

        self.assertEqual(table_a.get_height(), 2)
        self.assertEqual(table_b.get_height(), 1)
        self.assertEqual(table_c.get_height(), 0)

    def test_table_height2(self):
        """
        A - (B, C) -D
        """
        table_a = Table(table_name="A", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int),
        ], data_sizes=[100], data_paths=[""], annotations=[])

        table_b = Table(table_name="B", columns=[
            Column(name="a", column_type=TypeEnum.int),
        ], data_sizes=[100], data_paths=[""], annotations=[])

        table_c = Table(table_name="C", columns=[
            Column(name="b", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ], data_sizes=[100], data_paths=[""], annotations=[])

        table_d = Table(table_name="d", columns=[
            Column(name="c", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ], data_sizes=[100], data_paths=[""], annotations=[])

        table_a.join(table_b, "a", "a")
        table_a.join(table_c, "c", "c")
        table_c.join(table_d, "c", "c")

        self.assertEqual(table_a.get_height(), 2)
