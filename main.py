import sqlparse
from codegen.codegen import Parser
from codegen.table.column import TypeEnum
from codegen.table.table import Table, Column

sql = """
select
   l_orderkey,
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

"""

CUSTOMER_TABLE = Table(table_name="CUSTOMER", columns=[Column(name="c_custkey", column_type=TypeEnum.int)])
ORDERS_TABLE = Table(table_name="ORDERS", columns=[Column(name="o_custkey", column_type=TypeEnum.int),
                                                   Column(name="o_orderkey", column_type=TypeEnum.int)])
LINEITEM_TABLE = Table(table_name="LINEITEM", columns=[Column(name="l_orderkey", column_type=TypeEnum.int)])

parser = Parser(sql=sql, tables=[CUSTOMER_TABLE, ORDERS_TABLE, LINEITEM_TABLE], table_to_reveal=LINEITEM_TABLE)
parser.parse().to_file("/Users/liqiwei/Dropbox/classes/HKUST/Project 1/codegen/test.cpp")
