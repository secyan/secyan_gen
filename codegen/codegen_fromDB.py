from typing import List, Optional

from sqlparse.sql import IdentifierList, Identifier, Token

from .database.baseDB import DatabaseDriver
from .database.dbplan import DBPlan
from .free_connex_codegen import FreeConnexParser
from .node.cpp_nodes import FromNode, SelectNode
from codegen.node.cpp_nodes.JoinNode import JoinNode
from .table.table import Table


class CodeGenDB(FreeConnexParser):
    """
    This codegen use system's query execution plan to generate a code.
    """

    def __init__(self, sql: str, db_driver: DatabaseDriver, tables: List[Table], annotation_name: str):
        """
        Construct the Codegen DB Parser.

        :param sql: SQL Query
        :param db_driver: DB Driver which used to connect to the db
        :param tables: list of database tables
        """

        super().__init__(sql=sql, tables=tables, annotation_name=annotation_name)
        self.db_driver: DatabaseDriver = db_driver

    def parse(self, query_plan: Optional[DBPlan] = None):
        """
        Parse the sql string. If the query_plan is given, then use the given query plan.
        The query plan will provide join results as well as selections

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
        has_join_node = False
        select_node = None
        while cur:
            if isinstance(cur, SelectNode):
                select_node = cur
            if not isinstance(cur, JoinNode):
                cur.merge()
            else:
                has_join_node = True
            cur = cur.next

        # Sometimes, we perform join operation inside from node
        if not has_join_node:
            join_node = JoinNode(tables=self.tables, join_list=[])
            original = select_node.next
            # If select node does have next node
            if original:
                join_node.next = original
                join_node.next.prev = join_node

                select_node.next = join_node
                select_node.next.prev = select_node
