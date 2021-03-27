from typing import List

from codegen.table.table import Table


class DBPlan:
    def __init__(self, tables: List[Table]):
        self.tables: List[Table] = tables

    def perform_join(self):
        """
        Do the join operation on tables.
        :return:
        """
        raise NotImplementedError
