from typing import List, Optional

from sqlparse.sql import IdentifierList, Identifier, Token

from .codegen import Parser
from .database.baseDB import DatabaseDriver
from .database.dbplan import DBPlan
from .free_connex_codegen import FreeConnexParser
from .node import FromNode
from .node.JoinNode import JoinNode
from .table.table import Table


class CodeGenDB(FreeConnexParser):
    """
    This codegen use system's query execution plan to generate a code.
    """

    def __init__(self, sql: str, db_driver: DatabaseDriver, tables: List[Table]):
        """
        Construct the Codegen DB Parser.

        :param sql: SQL Query
        :param db_driver: DB Driver which used to connect to the db
        :param tables: list of database tables
        """

        super().__init__(sql=sql, tables=tables)
        self.db_driver: DatabaseDriver = db_driver

    def parse(self, query_plan: Optional[DBPlan] = None):
        """
        Parse the sql string. If the query_plan is given, then use the given query plan

        :param query_plan:
        :return:
        """
        if not query_plan:
            self.db_driver.plan = self.db_driver.get_query_plan(sql=self.sql)
        else:
            self.db_driver.plan = query_plan

        super(CodeGenDB, self).parse()

        self.db_driver.perform_join_by_plan(self.db_driver.plan, is_free_connex_table=self.is_free_connex)

        return self

    def __parse_from__(self):
        from_tables = [Identifier(tokens=[Token(value=f.variable_table_name, ttype="")]) for f in
                       self.db_driver.perform_select_from()]
        from_node = FromNode(tables=self.tables)
        from_node.set_identifier_list(from_tables)
        last = self.root.get_last_node()
        last.next = from_node
        last.next.prev = last

    def __parse_identifier__(self, token: Identifier):
        last = self.root.get_last_node()
        if isinstance(last, FromNode):
            return
        super().__parse_identifier__(token)

    def __parse_identifier_list__(self, token: IdentifierList):
        last = self.root.get_last_node()
        if isinstance(last, FromNode):
            return
        super().__parse_identifier_list__(token)

    def __do_merge__(self):
        cur = self.root
        while cur:
            if not isinstance(cur, JoinNode):
                cur.merge()
            cur = cur.next
