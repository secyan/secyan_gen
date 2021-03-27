from typing import Dict, List

from codegen.database.dbplan import DBPlan
from codegen.table.table import Table


class DatabaseDriver:
    """
    Base class for database driver. Implement this for other database backend.
    """

    def __init__(self, tables: List[Table]):
        self.tables = tables

    def get_query_plan(self, sql: str) -> DBPlan:
        """
        Return the query execution plan based on the sql string
        :param sql: sql query
        :return: a query execution plan
        """
        raise NotImplementedError

    def perform_join(self, sql: str):
        """
        Join table based on the sql string.
        This function will first call the database to get execution plan, and then use that plan to perform join.
        :param sql: Sql query
        :return:
        """
        plan = self.get_query_plan(sql)
        plan.perform_join()

    def perform_join_by_plan(self, plan: DBPlan):
        """
        Do the join by given a db plan.
        :param plan: DB Execution plan
        :return:
        """
        plan.perform_join()
