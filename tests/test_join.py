import unittest

from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table


class JoinTest(unittest.TestCase):
    """
    Test join on tables
    """

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

    def test_simple_join_3(self):
        self.a_table.join(self.b_table, "id", "id")
        self.b_table.join(self.c_table, "id", "id")
        column_names = self.a_table.column_names
        self.assertEqual(len(column_names), 5)
        expected_names = ["a.name", "a.id", "b.name", "c.name", "c.address"]
        for c in column_names:
            self.assertTrue(c.name_with_table in expected_names)

    def test_get_aggregate_columns(self):
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
        table_c.join(table_a, "e", "e")

        column_names = table_a.column_names
        self.assertEqual(len(column_names), 4)

        agg = table_b.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, "e")

        agg = table_a.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, "e")

        agg = table_c.get_aggregate_columns()
        self.assertEqual(0, len(agg))

    def test_get_aggregate_columns2(self):
        table_a = Table(table_name="A", columns=[
            Column(name="aa", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ])

        table_b = Table(table_name="B", columns=[
            Column(name="ba", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ])

        table_a.join(to_table=table_b, from_table_key="aa", to_table_key="ba")

        column_names = table_a.column_names
        self.assertEqual(len(column_names), 4)

        agg = table_b.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, "ba")
