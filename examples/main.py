import sqlparse
from codegen.codegen import Parser
from codegen.table.column import TypeEnum
from codegen.table.table import Table, Column
import json

sql = """
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

sql2 = """
select
   c_custkey,
   c_name,
   sum(l_extendedprice * (1 - l_discount)) as revenue,
   c_nationkey
 from
   CUSTOMER,
   ORDERS,
   LINEITEM
where
   c_custkey = o_custkey
   and l_orderkey = o_orderkey
   and o_orderdate >= date '1993-08-01'
   and o_orderdate < date '1993-08-01' + interval '3' month
   and l_returnflag = 'R'
 group by
   c_custkey,
   c_name
order by
   revenue desc
limit
   20;

"""

# CUSTOMER_TABLE = Table(table_name="CUSTOMER",
#                        columns=[
#                            Column(name="c_custkey", column_type=TypeEnum.int),
#                            Column(name="c_nationkey", column_type=TypeEnum.int)
#                        ])
# ORDERS_TABLE = Table(table_name="ORDERS",
#                      columns=[
#                          Column(name="o_custkey", column_type=TypeEnum.int),
#                          Column(name="o_orderkey", column_type=TypeEnum.int),
#                          Column(name="o_shippriority", column_type=TypeEnum.int)
#                      ])
# LINEITEM_TABLE = Table(table_name="LINEITEM",
#                        columns=[
#                            Column(name="l_orderkey", column_type=TypeEnum.int)
#                        ])
#
# SUPPLIER_TABLE = Table(table_name="SUPPLIER",
#                        columns=[
#                            Column(name="s_suppkey", column_type=TypeEnum.int),
#                            Column(name="s_nationkey", column_type=TypeEnum.int)
#                        ])
#
# NATION_TABLE = Table(table_name="NATION",
#                        columns=[
#                            Column(name="s_suppkey", column_type=TypeEnum.int),
#                            Column(name="s_nationkey", column_type=TypeEnum.int)
#                        ])

with open("examples/table_config.json", 'r') as f:
    tables = [Table.load_from_json(t) for t in json.load(f)]
    parser = Parser(sql=sql2, tables=tables)
    parser.parse().to_file("examples/test.cpp")
