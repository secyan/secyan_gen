from typing import List, Callable

from sqlparse.sql import Identifier, Comparison

from .FreeConnexJoinNode import FreeConnexJoinNode
from .JoinNode import JoinNode, JoinData
from ..table.table import Table


class WhereNode(FreeConnexJoinNode):
    def __init__(self, comparison_list: List[Comparison], tables: List[Table],
                 is_free_connex_table: Callable[[], bool]):
        join_list = [JoinData(left=c.left, right=c.right) for c in comparison_list if "=" in c.normalized]
        super().__init__(join_list, tables, is_free_connex_table)
        self.self_identify = "Where"
        self.from_tables: List[Identifier] = []
        self.tables = tables
