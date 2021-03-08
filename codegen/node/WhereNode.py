from typing import List

from sqlparse.sql import Identifier, Comparison

from .JoinNode import JoinNode, JoinData
from ..table.table import Table


class WhereNode(JoinNode):
    def __init__(self, comparison_list: List[Comparison], tables: List[Table]):
        join_list = [JoinData(left=c.left, right=c.right) for c in comparison_list if "=" in c.normalized]
        super().__init__(join_list=join_list, tables=tables)
        self.self_identify = "Where"
        self.from_tables: List[Identifier] = []
        self.tables = tables
