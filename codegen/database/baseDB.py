from typing import Dict, List, Optional, Callable, Tuple

from codegen.database.dbplan import DBPlan
from codegen.table.table import Table


class DatabaseDriver:
    """
    Base class for database driver. Implement this for other database backend.
    """

    def __init__(self, tables: List[Table]):
        self.tables = tables
        self.plan: Optional[DBPlan] = None

    def get_query_plan(self, sql: str) -> DBPlan:
        """
        Return the query execution plan based on the sql string

        :param sql: sql query
        :return: a query execution plan
        """
        raise NotImplementedError

    def perform_join_by_plan(self, plan: DBPlan, is_free_connex_table: Callable[[], Tuple[bool, List[Table]]]):
        """
        Do the join by a given db plan.

        :param is_free_connex_table:
        :param plan: DB Execution plan
        :return:
        """
        assert plan is not None

        plan.perform_join(is_free_connex_table=is_free_connex_table)
        self.plan = plan

    def perform_select_from(self):
        assert self.plan is not None
        return self.plan.perform_select_from()

    def execute(self, sql: str) -> List[Tuple]:
        raise NotImplementedError

    def execute_save(self, sql: str, output_filename: str):
        """
        Save sql result into a tbl file
        :param output_filename:
        :param sql:
        :return:
        """
        raise NotImplementedError
