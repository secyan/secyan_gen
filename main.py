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
   o_custkey = c_custkey 
   and o_orderkey = l_orderkey
group by
   l_orderkey,
   o_orderdate,
   o_shippriority

"""

CUSTOMER_TABLE = Table(table_name="CUSTOMER", columns=[Column(name="c_custkey", column_type=TypeEnum.int)])
ORDERS_TABLE = Table(table_name="ORDERS", columns=[Column(name="o_custkey", column_type=TypeEnum.int),
                                                   Column(name="o_orderkey", column_type=TypeEnum.int),
                                                   Column(name="o_shippriority", column_type=TypeEnum.int)])
LINEITEM_TABLE = Table(table_name="LINEITEM", columns=[Column(name="l_orderkey", column_type=TypeEnum.int)])

parser = Parser(sql=sql, tables=[CUSTOMER_TABLE, ORDERS_TABLE, LINEITEM_TABLE])
parser.parse().to_file("/Users/liqiwei/Dropbox/classes/HKUST/Project 1/codegen/test.cpp")
