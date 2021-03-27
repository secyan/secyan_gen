import json

from codegen.codegen_fromDB import CodeGenDB
from codegen.database.postgresDB import PostgresDBDriver
from os import getenv
from pprint import pprint

from codegen.table.table import Table

sql = """
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
   c_name,
   c_nationkey
order by
   revenue desc
limit
   20;
"""

if __name__ == '__main__':
    password = getenv('password')
    user = getenv('user')
    database = "tpch"
    host = "localhost"
    port = "5432"
    with open("./table_config.json", 'r') as f:
        tables = [Table.load_from_json(t) for t in json.load(f)]
        driver = PostgresDBDriver(password=password, user=user, database_name=database, host=host, port=port,
                                  tables=tables)

        codegen = CodeGenDB(sql=sql, db_driver=driver, tables=tables)
        codegen.parse().to_file("db-test.cpp")
