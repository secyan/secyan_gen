from copy import deepcopy
from typing import List

from jinja2 import Template
from sqlparse.sql import Comparison

from .BaseNode import BaseNode
from .SelectNode import SelectNode
from ..table.table import Table


class JoinData:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class JoinNode(BaseNode):

    def __init__(self, join_list: List[JoinData], tables: List[Table]):
        super().__init__()
        self.join_list: List[JoinData] = join_list
        self.tables = tables

    def __get_select__(self):
        cur = self
        while cur:
            if type(cur) == SelectNode:
                return cur
            cur = cur.prev

    def to_code(self):
        code = []
        selections = [i.normalized for i in self.__get_select__().identifier_list]
        template = Template(self.open_template_file("join.template.j2"))

        for c in self.join_list:
            c: JoinData
            left_table = None
            right_table = None
            for table in self.tables:
                column_names = [t.name for t in table.column_names]

                if str(c.right) in column_names and not right_table:
                    right_table = table
                    continue

                if str(c.left) in column_names and not left_table:
                    left_table = table

            if left_table and right_table:
                left_table.join(right_table, str(c.left), str(c.right))
                column_names = left_table.column_names
                not_in_names = []
                for column_name in column_names:
                    if column_name.name not in selections:
                        not_in_names.append(column_name.name)

                rendered = template.render(left_table=left_table, right_table=right_table,
                                           not_in_names=not_in_names, left=c.left, right=c.right,
                                           should_aggregate=len(not_in_names) > 0)
                code.append(rendered)

            return code
