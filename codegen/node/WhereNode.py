from typing import List, Callable, Tuple

from sqlparse.sql import Identifier, Comparison

from .FreeConnexJoinNode import FreeConnexJoinNode
from .JoinNode import JoinNode, JoinData
from ..table.table import Table


class WhereNode(JoinNode):
    def __init__(self, comparison_list: List[Comparison], tables: List[Table]):
        join_list = [JoinData(left_key=c.left, right_key=c.right) for c in comparison_list if "=" in c.normalized]
        super().__init__(join_list, tables)
        self.self_identify = "Where"
        self.from_tables: List[Identifier] = []
        self.tables = tables


class FreeConnexWhereNode(FreeConnexJoinNode):
    def __init__(self, comparison_list: List[Comparison], tables: List[Table],
                 is_free_connex_table: Callable[[], Tuple[bool, List[Table]]]):
        join_list = [JoinData(left_key=c.left, right_key=c.right) for c in comparison_list if "=" in c.normalized]
        super().__init__(join_list, tables, is_free_connex_table)
        self.self_identify = "Where"
        self.from_tables: List[Identifier] = []
        self.tables = tables
