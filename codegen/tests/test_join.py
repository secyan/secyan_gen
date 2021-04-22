import unittest

from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table
from codegen.table.free_connex_table import FreeConnexTable
from .test_table_config import TEST_CONFIG
from ..codegen import Parser
from ..free_connex_codegen import FreeConnexParser


class JoinTest(unittest.TestCase):
    """
    Test join on tables
    """

    def setUp(self):
        self.a_table = Table(table_name="a",
                             columns=[Column(name="name", column_type=TypeEnum.string),
                                      Column(name="id", column_type=TypeEnum.int)], data_sizes=[100])
        self.b_table = Table(table_name="b", columns=[Column(name="name", column_type=TypeEnum.string),
                                                      Column(name="id", column_type=TypeEnum.int)], data_sizes=[100])

        self.c_table = Table(table_name="c", columns=[
            Column(name="name", column_type=TypeEnum.string),
            Column(name="id", column_type=TypeEnum.int),
            Column(name="address", column_type=TypeEnum.string)
        ], data_sizes=[100])

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

    def test_simple_join_with_error(self):
        self.assertRaises(RuntimeError, self.a_table.join, self.b_table, "id", "abc")

    def test_get_aggregate_columns(self):
        table_a = Table(table_name="A", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ], data_sizes=[100])

        table_b = Table(table_name="B", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ], data_sizes=[100])

        table_c = Table(table_name="C", columns=[
            Column(name="e", column_type=TypeEnum.int),
            Column(name="f", column_type=TypeEnum.int)
        ], data_sizes=[100])

        table_a.join(table_b, "a", "a")
        table_c.join(table_a, "e", "e")

        column_names = table_a.column_names
        self.assertEqual(len(column_names), 4)

        agg = table_b.get_aggregate_columns()
        self.assertEqual(2, len(agg))
        self.assertEqual(agg[0].name, "a")
        self.assertEqual(agg[1].name, "e")

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
        ], data_sizes=[100])

        table_b = Table(table_name="B", columns=[
            Column(name="ba", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ], data_sizes=[100])

        table_a.join(to_table=table_b, from_table_key="aa", to_table_key="ba")

        column_names = table_a.column_names
        self.assertEqual(len(column_names), 4)

        agg = table_b.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, "ba")

    def test_get_aggregate_columns3(self):
        table_a = Table(table_name="A", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
        ], data_sizes=[100])

        table_b = Table(table_name="B", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ], data_sizes=[100])

        table_c = Table(table_name="C", columns=[
            Column(name="b", column_type=TypeEnum.int),
            Column(name="d", column_type=TypeEnum.int)
        ], data_sizes=[100])

        table_a.join(table_b, 'a', 'a')
        table_a.join(table_c, 'b', 'b')

        agg = table_b.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, 'a')

        agg = table_c.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, "b")


class FreeConnexJoin(unittest.TestCase):

    def setUp(self) -> None:
        self.table_1 = FreeConnexTable(table_name="1", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
        ], data_sizes=[100])

        self.table_2 = FreeConnexTable(table_name="2", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ], data_sizes=[100])

        self.table_3 = FreeConnexTable(table_name="3", columns=[
            Column(name="b", column_type=TypeEnum.int),
            Column(name="d", column_type=TypeEnum.int)
        ], data_sizes=[100])

        self.table_4 = FreeConnexTable(table_name="4", columns=[
            Column(name="d", column_type=TypeEnum.int),
            Column(name="f", column_type=TypeEnum.int),
            Column(name="g", column_type=TypeEnum.int),
        ], data_sizes=[100])

        self.table_5 = FreeConnexTable(table_name="5", columns=[
            Column(name="b", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ], data_sizes=[100])

    def test_is_free_connex_join(self):
        """
        See exaample/join_tree.drawio tree A
        :return:
        """

        self.table_1.join(self.table_2, "a", "a")
        self.table_1.join(self.table_3, "b", "b")
        self.table_3.join(self.table_4, "d", "d")
        self.table_3.join(self.table_5, "b", "b")

        output_attrs = ["b", "d", "e", "f"]
        non_output_attrs = ["a", "c", "g"]

        height_of_tree = self.table_1.get_height()

        table, height = self.table_1.get_highest_with_attr("a", height_of_tree)
        self.assertEqual(table, self.table_1)
        self.assertEqual(height, 2)

        table, height = self.table_1.get_highest_with_attr("d", height_of_tree)
        self.assertEqual(table, self.table_3)
        self.assertEqual(height, 1)

        table, height = self.table_1.get_highest_with_attr("c", height_of_tree)
        self.assertEqual(table, self.table_2)
        self.assertEqual(height, 1)

        is_free_connex, output_tables = self.table_1.is_free_connex(output_attrs=output_attrs,
                                                                    non_output_attrs=non_output_attrs,
                                                                    height=height_of_tree)
        self.assertFalse(is_free_connex)
        self.assertEqual(output_tables[0], self.table_3)

    def test_is_free_connex_join2(self):
        """
        See exaample/join_tree.drawio tree B
        :return:
        """

        self.table_5.join(self.table_3, "b", "b")
        self.table_3.join(self.table_1, "b", "b")
        self.table_1.join(self.table_2, "a", "a")
        self.table_3.join(self.table_4, "d", "d")

        output_attrs = ["b", "d", "e", "f"]
        non_output_attrs = ["a", "c", "g"]

        height_of_tree = self.table_5.get_height()

        table, height = self.table_5.get_highest_with_attr("a", height_of_tree)
        self.assertEqual(table, self.table_1)
        self.assertEqual(height, 1)

        table, height = self.table_5.get_highest_with_attr("d", height_of_tree)
        self.assertEqual(table, self.table_3)
        self.assertEqual(height, 2)

        table, height = self.table_5.get_highest_with_attr("c", height_of_tree)
        self.assertEqual(table, self.table_2)
        self.assertEqual(height, 0)

        is_free_connex, _ = self.table_5.is_free_connex(output_attrs=output_attrs,
                                                        non_output_attrs=non_output_attrs,
                                                        height=height_of_tree)
        self.assertTrue(is_free_connex)

    def test_is_free_connex_join3(self):
        """
        See exaample/join_tree.drawio tree A
        :return:
        """

        self.table_1.join(self.table_2, "a", "a")
        self.table_1.join(self.table_3, "b", "b")
        self.table_3.join(self.table_4, "d", "d")
        self.table_3.join(self.table_5, "b", "b")

        output_attrs = ["b", "d", "e", "f"]
        non_output_attrs = ["a", "c", "g", "sum"]

        height_of_tree = self.table_1.get_height()

        is_free_connex, output_tables = self.table_1.is_free_connex(output_attrs=output_attrs,
                                                                    non_output_attrs=non_output_attrs,
                                                                    height=height_of_tree)
        self.assertFalse(is_free_connex)
        self.assertEqual(output_tables[0], self.table_3)

    def test_is_free_connex_join4(self):
        """
        See exaample/join_tree.drawio tree C
        :return:
        """
        self.table_1 = FreeConnexTable(table_name="1", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b1", column_type=TypeEnum.int),
        ], data_sizes=[100])

        self.table_2 = FreeConnexTable(table_name="2", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ], data_sizes=[100])

        self.table_3 = FreeConnexTable(table_name="3", columns=[
            Column(name="b2", column_type=TypeEnum.int),
            Column(name="d1", column_type=TypeEnum.int)
        ], data_sizes=[100])

        self.table_4 = FreeConnexTable(table_name="4", columns=[
            Column(name="d2", column_type=TypeEnum.int),
            Column(name="f", column_type=TypeEnum.int),
            Column(name="g", column_type=TypeEnum.int),
        ], data_sizes=[100])

        self.table_5 = FreeConnexTable(table_name="5", columns=[
            Column(name="b3", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ], data_sizes=[100])

        self.table_1.join(self.table_2, "a", "a")
        self.table_1.join(self.table_3, "b1", "b2")
        self.table_3.join(self.table_4, "d1", "d2")
        self.table_3.join(self.table_5, "b2", "b3")

        output_attrs = ["b1", "d1", "e", "f"]
        non_output_attrs = ["a", "c", "g"]

        height_of_tree = self.table_1.get_height()

        is_free_connex, output_tables = self.table_1.is_free_connex(output_attrs=output_attrs,
                                                                    non_output_attrs=non_output_attrs,
                                                                    height=height_of_tree)
        self.assertFalse(is_free_connex)
        self.assertEqual(output_tables[0], self.table_3)
        self.assertFalse(self.table_1.is_cycle())

    def test_swap(self):
        self.table_1.join(self.table_2, "a", "a")
        self.table_1.join(self.table_3, "b", "b")
        self.table_3.join(self.table_4, "d", "d")
        self.table_3.join(self.table_5, "b", "b")

        # self.table_3.swap()
        # self.assertEqual(self.table_5.parent, None)
        # self.assertEqual(self.table_5.children, [self.table_3])

    def test_is_cycle(self):
        table1 = FreeConnexTable(table_name="1", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
        ], data_sizes=[100])

        table2 = FreeConnexTable(table_name="2", columns=[
            Column(name="b", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int),
        ], data_sizes=[100])

        table3 = FreeConnexTable(table_name="3", columns=[
            Column(name="c", column_type=TypeEnum.int),
            Column(name="a", column_type=TypeEnum.int),
        ], data_sizes=[100])

        table1.join(table2, "b", "b")
        table2.join(table3, "c", "c")

        self.assertRaises(Exception, table3.join, table1, "a", "a")


class TestJoin2(unittest.TestCase):
    def test_simple_join(self):
        sql = """
        select
    n_name,
    sum(l_extendedprice * (1 - l_discount)) as revenue
from
    CUSTOMER,
    ORDERS,
    LINEITEM,
    SUPPLIER,
    NATION,
    REGION
where
     o_custkey=c_custkey
    and l_orderkey = o_orderkey
    and s_suppkey= l_suppkey
    and r_name = 'MIDDLE EAST'
    and o_orderdate >= date '1994-01-01'
    and o_orderdate < date '1994-01-01' + interval '1' year
group by
    n_name
order by
    revenue desc;
        """
        tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]
        parser = FreeConnexParser(tables=tables, sql=sql)
        parser.parse()
        root = parser.root_table
        self.assertTrue(parser.is_free_connex())
        # self.assertEqual("supplier", root.variable_table_name)
        # self.assertEqual("lineitem", root.children[0].to_table.variable_table_name)
