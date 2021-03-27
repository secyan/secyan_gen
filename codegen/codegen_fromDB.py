from typing import List, Optional

from .codegen import Parser
from .database.baseDB import DatabaseDriver
from .database.dbplan import DBPlan
from .node.JoinNode import JoinNode
from .table.table import Table


class CodeGenDB(Parser):
    """
    This codegen use system's query execution plan to generate a code.

    """

    def __init__(self, sql: str, db_driver: DatabaseDriver, tables: List[Table]):
        super().__init__(sql=sql, tables=tables)
        self.db_driver: DatabaseDriver = db_driver

    def parse(self, query_plan: Optional[DBPlan] = None):
        if query_plan:
            self.db_driver.perform_join_by_plan(query_plan)
        else:
            self.db_driver.perform_join(sql=self.sql)

        return super(CodeGenDB, self).parse()

    def do_merge(self):
        cur = self.root
        while cur:
            if not isinstance(cur, JoinNode):
                cur.merge()
            else:
                cur.root = self.root_table
            cur = cur.next
