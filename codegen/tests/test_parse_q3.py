import unittest

from codegen.codegen import Parser
from .base_test_case import QueryTestCase
from ..free_connex_codegen import FreeConnexParser
from ..node.SelectNode import SelectNode
from ..table.table import Table, CharacterEnum
from ..table.free_connex_table import FreeConnexTable
from .test_table_config import TEST_CONFIG


class TestParseQ3(QueryTestCase):
    def setUp(self) -> None:
        self.query = """
        select
           l_orderkey,
           sum(l_extendedprice * (1 - l_discount)) as revenue,
           o_orderdate,
           o_shippriority
        from
           CUSTOMER,
           ORDERS,
           LINEITEM
        where
           c_mktsegment = 'AUTOMOBILE'
           and c_custkey = o_custkey
           and l_orderkey = o_orderkey
           and o_orderdate < date '1995-03-13'
           and l_shipdate > date '1995-03-13'
        group by
           l_orderkey,
           o_orderdate,
           o_shippriority
        order by
           revenue desc,
           o_orderdate
        limit
           10;
        """

        self.tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]
        self.codegen = FreeConnexParser(tables=self.tables, sql=self.query)


    def test_q3(self):
        self.assertTrue(len(self.tables) > 0)
        self.codegen.parse()
        tables = self.codegen.tables

        CUSTOMRER = tables[1]
        LINEITEM = tables[2]
        ORDERS = tables[3]

        select_node: SelectNode = self.codegen.root.next
        where_node = select_node.next
        group_by_node = where_node.next
        order_by_node = group_by_node.next

        self.assertEqual(len(select_node.from_tables), 3)
        self.assertEqual(len(select_node.identifier_list), 4)
        self.assertFalse(tables[2].is_bool)

        code = where_node.to_code(ORDERS.get_root())
        self.assert_content_in_arr(code, 'vector<string> o_groupBy = { "o_orderkey","o_orderdate","o_shippriority" };')

        is_free, _ = self.codegen.is_free_connex()
        self.assertTrue(is_free)

        # self.assertEqual(CUSTOMRER.owner, CharacterEnum.server)
        # self.assertEqual(LINEITEM.owner, CharacterEnum.server)
        # self.assertEqual(ORDERS.owner, CharacterEnum.client)


class TestParseQ3ToFreeConnex(QueryTestCase):
    """
    Enumerate all possible joins and create a free connex join tree
    """

    def setUp(self) -> None:
        self.tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]

    def test_q3(self):
        """
        Join Tree should be a free connex join tree
        :return:
        """
        self.query = """
              select
                 l_orderkey,
                 sum(l_extendedprice * (1 - l_discount)) as revenue,
                 o_orderdate,
                 o_shippriority
              from
                 CUSTOMER,
                 ORDERS,
                 LINEITEM
              where
                 c_mktsegment = 'AUTOMOBILE'
                 and o_custkey = c_custkey
                 and o_orderkey = l_orderkey
                 and o_orderdate < date '1995-03-13'
                 and l_shipdate > date '1995-03-13'
              group by
                 l_orderkey,
                 o_orderdate,
                 o_shippriority
              order by
                 revenue desc,
                 o_orderdate
              limit
                 10;
              """
        self.codegen = FreeConnexParser(tables=self.tables, sql=self.query)
        self.assertTrue(len(self.tables) > 0)
        self.codegen.parse()
        tables = self.codegen.tables

        CUSTOMRER = tables[1]
        LINEITEM = tables[2]
        ORDERS = tables[3]

        select_node: SelectNode = self.codegen.root.next
        where_node = select_node.next
        group_by_node = where_node.next
        order_by_node = group_by_node.next

        self.assertEqual(len(select_node.from_tables), 3)
        self.assertEqual(len(select_node.identifier_list), 4)
        self.assertFalse(tables[2].is_bool)

        code = where_node.to_code(ORDERS.get_root())
        self.assert_content_in_arr(code, 'vector<string> o_groupBy = { "o_orderkey","o_orderdate","o_shippriority" };')

        is_free, _ = self.codegen.is_free_connex()
        self.assertTrue(is_free)

    def test_q32(self):
        """
        Join tree should be a free connex join tree
        :return:
        """
        self.query = """
              select
                 l_orderkey,
                 sum(l_extendedprice * (1 - l_discount)) as revenue,
                 o_orderdate,
                 o_shippriority
              from
                 CUSTOMER,
                 ORDERS,
                 LINEITEM
              where
                 c_mktsegment = 'AUTOMOBILE'
                 and o_custkey = c_custkey
                 and l_orderkey = o_orderkey
                 and o_orderdate < date '1995-03-13'
                 and l_shipdate > date '1995-03-13'
              group by
                 l_orderkey,
                 o_orderdate,
                 o_shippriority
              order by
                 revenue desc,
                 o_orderdate
              limit
                 10;
              """
        self.codegen = FreeConnexParser(tables=self.tables, sql=self.query)
        self.assertTrue(len(self.tables) > 0)
        self.codegen.parse()
        tables = self.codegen.tables

        CUSTOMRER = tables[1]
        LINEITEM = tables[2]
        ORDERS = tables[3]

        select_node: SelectNode = self.codegen.root.next
        where_node = select_node.next
        group_by_node = where_node.next
        order_by_node = group_by_node.next

        self.assertEqual(len(select_node.from_tables), 3)
        self.assertEqual(len(select_node.identifier_list), 4)
        self.assertFalse(tables[2].is_bool)

        code = where_node.to_code(ORDERS.get_root())
        self.assert_content_in_arr(code, 'vector<string> o_groupBy = { "o_orderkey","o_orderdate","o_shippriority" };')

        is_free, _ = self.codegen.is_free_connex()
        self.assertTrue(is_free)

    def test_q33(self):
        """
        Join tree should be a free connex join tree
        :return:
        """
        self.query = """
                 select
                    l_orderkey,
                    sum(l_extendedprice * (1 - l_discount)) as revenue,
                    o_orderdate,
                    o_shippriority
                 from
                    CUSTOMER,
                    ORDERS,
                    LINEITEM
                 where
                    c_mktsegment = 'AUTOMOBILE'
                    and c_custkey = o_custkey
                    and o_orderkey = l_orderkey
                    and o_orderdate < date '1995-03-13'
                    and l_shipdate > date '1995-03-13'
                 group by
                    l_orderkey,
                    o_orderdate,
                    o_shippriority
                 order by
                    revenue desc,
                    o_orderdate
                 limit
                    10;
                 """
        self.codegen = FreeConnexParser(tables=self.tables, sql=self.query)
        self.assertTrue(len(self.tables) > 0)
        self.codegen.parse()
        tables = self.codegen.tables

        CUSTOMRER = tables[1]
        LINEITEM = tables[2]
        ORDERS = tables[3]

        select_node: SelectNode = self.codegen.root.next
        where_node = select_node.next
        group_by_node = where_node.next
        order_by_node = group_by_node.next

        self.assertEqual(len(select_node.from_tables), 3)
        self.assertEqual(len(select_node.identifier_list), 4)
        self.assertFalse(tables[2].is_bool)

        code = where_node.to_code(ORDERS.get_root())
        self.assert_content_in_arr(code, 'vector<string> o_groupBy = { "o_orderkey","o_orderdate","o_shippriority" };')

        is_free, _ = self.codegen.is_free_connex()
        self.assertTrue(is_free)


class TestParseQuery(QueryTestCase):
    def setUp(self) -> None:
        self.query = """
      select
   l_orderkey,
   sum(l_extendedprice * (1 - l_discount)) as revenue,
   o_orderdate,
   o_shippriority
from
   CUSTOMER,
   ORDERS,
   LINEITEM
where
   c_mktsegment = 'AUTOMOBILE'
   and c_custkey = o_custkey
   and l_orderkey = o_orderkey
   and o_orderdate < date '1995-03-13'
   and l_shipdate > date '1995-03-13'
group by
   l_orderkey,
   o_orderdate,
   o_shippriority
order by
   revenue desc,
   o_orderdate
limit
   10;

        """

        self.tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]
        self.codegen = FreeConnexParser(tables=self.tables, sql=self.query)

    def test_q3(self):
        self.assertTrue(len(self.tables) > 0)
        self.codegen.parse()
        tables = self.codegen.tables

        CUSTOMRER = tables[1]
        LINEITEM = tables[2]
        ORDERS = tables[3]

        select_node: SelectNode = self.codegen.root.next
        where_node = select_node.next
        group_by_node = where_node.next
        order_by_node = group_by_node.next

        self.assertEqual(len(select_node.from_tables), 3)
        self.assertEqual(len(select_node.identifier_list), 4)
        self.assertFalse(tables[2].is_bool)

        is_free, _ = self.codegen.is_free_connex()
        self.assertTrue(is_free)
