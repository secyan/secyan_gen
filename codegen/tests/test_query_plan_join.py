from unittest import TestCase

from codegen.codegen_fromDB import CodeGenDB
from codegen.database.postgresDB import PostgresDBDriver, PostgresDBPlan
from codegen.table import FreeConnexTable
from codegen.tests.test_table_config import TEST_CONFIG

simple_plan = [{'Plan': {'Node Type': 'Limit', 'Parallel Aware': False, 'Startup Cost': 47843.7, 'Total Cost': 47843.72,
                         'Plan Rows': 10, 'Plan Width': 44, 'Plans': [
        {'Node Type': 'Sort', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Startup Cost': 47843.7,
         'Total Cost': 48152.37, 'Plan Rows': 123469, 'Plan Width': 44,
         'Sort Key': ["(sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))) DESC",
                      'orders.o_orderdate'], 'Plans': [
            {'Node Type': 'Aggregate', 'Strategy': 'Sorted', 'Partial Mode': 'Finalize', 'Parent Relationship': 'Outer',
             'Parallel Aware': False, 'Startup Cost': 28926.68, 'Total Cost': 45175.58, 'Plan Rows': 123469,
             'Plan Width': 44, 'Group Key': ['lineitem.l_orderkey', 'orders.o_orderdate', 'orders.o_shippriority'],
             'Plans': [{'Node Type': 'Gather Merge', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                        'Startup Cost': 28926.68, 'Total Cost': 42346.09, 'Plan Rows': 102890, 'Plan Width': 44,
                        'Workers Planned': 2, 'Plans': [
                     {'Node Type': 'Aggregate', 'Strategy': 'Sorted', 'Partial Mode': 'Partial',
                      'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Startup Cost': 27926.66,
                      'Total Cost': 29470.01, 'Plan Rows': 51445, 'Plan Width': 44,
                      'Group Key': ['lineitem.l_orderkey', 'orders.o_orderdate', 'orders.o_shippriority'], 'Plans': [
                         {'Node Type': 'Sort', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                          'Startup Cost': 27926.66, 'Total Cost': 28055.27, 'Plan Rows': 51445, 'Plan Width': 24,
                          'Sort Key': ['lineitem.l_orderkey', 'orders.o_orderdate', 'orders.o_shippriority'], 'Plans': [
                             {'Node Type': 'Hash Join', 'Parent Relationship': 'Outer', 'Parallel Aware': True,
                              'Join Type': 'Inner', 'Startup Cost': 8792.41, 'Total Cost': 23900.89, 'Plan Rows': 51445,
                              'Plan Width': 24, 'Inner Unique': False,
                              'Hash Cond': '(lineitem.l_orderkey = orders.o_orderkey)', 'Plans': [
                                 {'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': True,
                                  'Relation Name': 'lineitem', 'Alias': 'lineitem', 'Startup Cost': 0.0,
                                  'Total Cost': 14386.98, 'Plan Rows': 135237, 'Plan Width': 16,
                                  'Filter': "(l_shipdate > '1995-03-13'::date)"},
                                 {'Node Type': 'Hash', 'Parent Relationship': 'Inner', 'Parallel Aware': True,
                                  'Startup Cost': 8491.74, 'Total Cost': 8491.74, 'Plan Rows': 24054, 'Plan Width': 12,
                                  'Plans': [{'Node Type': 'Hash Join', 'Parent Relationship': 'Outer',
                                             'Parallel Aware': False, 'Join Type': 'Inner', 'Startup Cost': 1169.33,
                                             'Total Cost': 8491.74, 'Plan Rows': 24054, 'Plan Width': 12,
                                             'Inner Unique': False,
                                             'Hash Cond': '(orders.o_custkey = customer.c_custkey)', 'Plans': [
                                          {'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer',
                                           'Parallel Aware': True, 'Relation Name': 'orders', 'Alias': 'orders',
                                           'Startup Cost': 0.0, 'Total Cost': 6782.5, 'Plan Rows': 59875,
                                           'Plan Width': 16, 'Filter': "(o_orderdate < '1995-03-13'::date)"},
                                          {'Node Type': 'Hash', 'Parent Relationship': 'Inner', 'Parallel Aware': False,
                                           'Startup Cost': 1094.0, 'Total Cost': 1094.0, 'Plan Rows': 6026,
                                           'Plan Width': 4, 'Plans': [
                                              {'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer',
                                               'Parallel Aware': False, 'Relation Name': 'customer',
                                               'Alias': 'customer', 'Startup Cost': 0.0, 'Total Cost': 1094.0,
                                               'Plan Rows': 6026, 'Plan Width': 4,
                                               'Filter': "(c_mktsegment = 'AUTOMOBILE'::bpchar)"}]}]}]}]}]}]}]}]}]}]}}]

SQL = """
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
   and o_custkey=c_custkey 
   and o_orderkey= l_orderkey 
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


class TestQueryPlanJoin(TestCase):

    def setUp(self) -> None:
        self.tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]

    def test_simple_join(self):
        db_plan = PostgresDBPlan.from_json(simple_plan[0]['Plan'], tables=self.tables)
        db_driver = PostgresDBDriver(host="", database_name="", user="", password="", port="", tables=self.tables)
        codegen = CodeGenDB(sql=SQL, db_driver=db_driver, tables=self.tables)
        codegen.parse(query_plan=db_plan)
        root = codegen.root_table
        self.assertEqual("orders", root.variable_table_name)
        self.assertTrue(codegen.is_free_connex())
