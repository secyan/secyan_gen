from typing import List

from sqlparse.sql import Identifier, Comparison

from .BaseNode import BaseNode
from ..table.table import Table


class WhereNode(BaseNode):
    def __init__(self, comparison_list: List[Comparison], tables: List[Table]):
        super().__init__()
        self.self_identify = "Where"
        self.from_tables: List[Identifier] = []
        self.comparison_list: List[Comparison] = comparison_list
        self.tables = tables

    def to_code(self) -> List[str]:
        code = []
        for c in self.comparison_list:
            c: Comparison
            if "=" in c.value:
                left_table = None
                right_table = None
                for table in self.tables:
                    column_names = [t.name for t in table.column_names]

                    if str(c.right) in column_names:
                        right_table = table

                    if str(c.left) in column_names:
                        left_table = table

                if left_table and right_table:
                    tmp_code = f"{left_table.variable_table_name}.SemiJoin({right_table.variable_table_name},{c.left} , {c.right});"

                    code.append(tmp_code)
        return code
