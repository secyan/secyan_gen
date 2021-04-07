from typing import List, Callable

from sqlparse.sql import Identifier

from .JoinNode import JoinNode, JoinData
from ..table import FreeConnexTable, Table


class FreeConnexJoinNode(JoinNode):

    def __init__(self, join_list: List[JoinData], tables: List[Table], is_free_connex_table: Callable[[], bool]):
        super().__init__(join_list, tables)
        self.is_free_connex_table = is_free_connex_table

    def merge(self):
        for i in range(0, len(self.join_list), 2):
            self.__perform_join__(i)
            is_free_connex, _ = self.is_free_connex_table()
            if not is_free_connex:
                if i == len(self.join_list) - 1:
                    pass

                else:
                    self.__clear_join__()
            else:
                break

    def __perform_join__(self, index: int):
        """
        Join two tables. If the current index of table less than the index, the perform left join right,
        otherwise, right to left
        :param index: current index
        :return:
        """
        for i, c in enumerate(self.join_list):
            c: JoinData
            left_table = None
            right_table = None
            for table in self.tables:
                column_names = [t.name for t in table.original_column_names]

                if str(c.right) in column_names and not right_table:
                    right_table = table
                    continue

                if str(c.left) in column_names and not left_table:
                    left_table = table

            if left_table and right_table:
                if i > index:
                    right_table.join(left_table, str(c.right), str(c.left))
                else:
                    left_table.join(right_table, str(c.left), str(c.right))
                left_table.used_in_join = True
                right_table.used_in_join = True
                # left_table.join(right_table, str(c.left), str(c.right))
                if left_table not in self.join_tables:
                    self.join_tables.append(left_table)

                if right_table not in self.join_tables:
                    self.join_tables.append(right_table)

            else:
                if not left_table and type(c.left) is Identifier:
                    raise RuntimeError(f"Cannot find related join column: {c.left}")
                elif not right_table and type(c.right) is Identifier:
                    raise RuntimeError(f"Cannot find related join column: {c.right}")

    def __clear_join__(self):
        """
        Clear all join
        :return:
        """
        for table in self.join_tables:
            table.clear_join()

        self.join_tables = []
