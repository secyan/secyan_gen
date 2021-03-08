from copy import deepcopy
from typing import List

from jinja2 import Template
from sqlparse.sql import Comparison

from .BaseNode import BaseNode
from .SelectNode import SelectNode
from ..table.column import Column, TypeEnum
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
        tables = []
        index = []

        for i, c in enumerate(self.join_list):
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
                if left_table not in tables:
                    tables.append(left_table)
                    index.append(i)

                if right_table not in tables:
                    tables.append(right_table)
                    index.append(i)

        root = None
        for table in tables:
            if not table.parent:
                root = table
                break

        code = self.to_code_util(root=root)
        return code

    def to_code_util(self, root: Table, from_key=None, to_key=None) -> List[str]:
        """
        Do a post-order tree Traversal to generate code
        :param root: current table
        :param from_key: join key. From table's column name
        :param to_key: join key. To table's column name
        :return: list of generated code
        """
        code = []
        template = Template(self.open_template_file("join.template.j2"))
        for child in root.children:
            code += self.to_code_util(child.to_table, child.from_table_key, child.to_table_key)

        if root.parent:
            agg = root.get_aggregate_columns()
            rendered = template.render(left_table=root.parent, right_table=root,
                                       aggregate=agg, left=from_key, right=to_key,
                                       should_aggregate=len(agg) > 0, should_join=True)

            code += rendered.split("\n")

        else:
            # TODO: Conditional aggregate. Currently will append aggregate statement no matter what.
            selections = [i.normalized for i in self.__get_select__().identifier_list]
            agg = [Column(name=s, column_type=TypeEnum.int) for s in selections]

            rendered = template.render(left_table=root.parent, right_table=root,
                                       aggregate=agg, left=from_key, right=to_key,
                                       should_aggregate=True, should_join=False, reveal_table=root, should_reveal=True)
            code += rendered.split("\n")

        return code
