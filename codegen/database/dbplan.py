from typing import List, Callable, Tuple

from codegen.table.table import Table


class DBPlan:
    def __init__(self, tables: List[Table]):
        self.tables: List[Table] = tables

    def perform_join(self, is_free_connex_table: Callable[[], Tuple[bool, List[Table]]]):
        """
        Do the join operation on tables.
        :return:
        """
        raise NotImplementedError

    def perform_select_from(self) -> List[Table]:
        """
        Get tables needed for codegen
        :return:
        """
        raise NotImplementedError
