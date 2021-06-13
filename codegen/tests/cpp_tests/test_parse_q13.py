from os import getenv

from codegen.codegen_fromDB import CodeGenDB
from codegen.database.postgresDB import PostgresDBDriver
from codegen.table import FreeConnexTable
from codegen.tests.basic_tests.base_test_case import DBTestCase
from codegen.tests.test_table_config import TEST_CONFIG

query = """
select
    c_count,
    count(*) as custdist
from
    (
        select
            c_custkey,
            count(o_orderkey) as c_count
        from
            CUSTOMER
            left outer join ORDERS on c_custkey = o_custkey
            and o_comment not like '%pending%deposits%'
        group by
            c_custkey
    ) c_orders
group by
    c_count
order by
    custdist desc,
    c_count desc;
"""


class TestParseQ13(DBTestCase):
    def setUp(self):
        super().setUp()

        password = getenv('password')
        user = getenv('user')
        database = getenv("database")
        host = getenv("host")
        port = getenv("port")
        self.tables = [FreeConnexTable.load_from_json(t) for t in TEST_CONFIG]

        self.driver = PostgresDBDriver(password=password,
                                       user=user,
                                       database_name=database,
                                       host=host,
                                       port=port,
                                       tables=self.tables)

    def test_simple_parse(self):
        """
        Test if join statement in the generated code
        :return:
        """
        parser = CodeGenDB(db_driver=self.driver, sql=query, tables=self.tables, annotation_name="demo")
        code = parser.parse().to_output()
        self.assert_content_in("orders.Aggregate", code)
