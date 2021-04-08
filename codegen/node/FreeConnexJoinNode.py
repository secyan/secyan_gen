from math import factorial
from typing import List, Callable, Tuple
from sqlparse.sql import Identifier
import itertools
from .JoinNode import JoinNode, JoinData
from ..table import FreeConnexTable, Table


class FreeConnexJoinNode(JoinNode):
    """
    A join node which will try to create a free connex join. However, it won't guarantee the generated
    join tree will be a free connex join tree.
    """

    def __init__(self, join_list: List[JoinData], tables: List[Table],
                 is_free_connex_table: Callable[[], Tuple[bool, List[Table]]]):
        """
        Initialize a Free Connex Join Node.

        :param join_list: a list of join data. Included left key, right key.
        :param tables: A list of tables
        :param is_free_connex_table: A function which can be used to test if one join tree is a free connex join tree
        """

        super().__init__(join_list, tables)
        self.is_free_connex_table = is_free_connex_table

    def merge(self):
        """
        Enumerate all possible join trees in order to find the free connex join tree
        :return:
        """
        self.preprocess_join_list()
        length = len(self.join_list)

        # Will generate a list of combinations with 0 and 1
        # 0 means will perform left to right join
        # 1 means will perform right to left join
        # this will let the program enumerate all the possible join trees
        # in order to find the free connex join tree
        combinations = list(itertools.product([0, 1],  repeat=length))

        for i, combination in enumerate(combinations):
            # (0, 0, 0)
            combination: Tuple[int]

            self.__perform_join__(combination)
            is_free_connex, _ = self.is_free_connex_table()
            if not is_free_connex:
                if i == len(combinations) - 1:
                    pass

                else:
                    self.__clear_join__()
            else:
                break

    def __perform_join__(self, combination: Tuple[int]):
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
                if combination[i] == 1:
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
