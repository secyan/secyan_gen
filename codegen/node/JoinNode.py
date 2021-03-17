from typing import List

from jinja2 import Template

from .BaseNode import BaseNode
from .GroupbyNode import GroupByNode
from .SelectNode import SelectNode
from ..table.column import Column, TypeEnum
from ..table.table import Table


class JoinData:
    def __init__(self, left, right):
        """
        Data object contains join info
        :param left: key on the left join statement
        :param right: key on the right join statement
        """
        self.left = left
        self.right = right


class JoinNode(BaseNode):

    def __init__(self, join_list: List[JoinData], tables: List[Table]):
        """
        Base node which perform join operation
        :param join_list:
        :param tables:
        """
        super().__init__(tables=tables)
        self.join_list: List[JoinData] = join_list
        self.tables = tables
        self.join_tables: List[Table] = []

    def __get_select__(self):
        """
        Get the select node from the SQL tree
        :return:
        """
        cur = self
        while cur:
            if type(cur) == SelectNode:
                return cur
            cur = cur.prev

    def __get_group_by__(self):
        """
        Get the group by node from the SQL tree
        :return:
        """
        cur = self
        while cur:
            if type(cur) == GroupByNode:
                return cur
            cur = cur.next

    def merge(self):
        """
        Perform join
        :return:
        """
        
        # TODO: Generate a free-connex join tree
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
                right_table.join(left_table, str(c.right), str(c.left))
                # left_table.join(right_table, str(c.left), str(c.right))
                if left_table not in self.join_tables:
                    self.join_tables.append(left_table)

                if right_table not in self.join_tables:
                    self.join_tables.append(right_table)

    def to_code(self):
        root = self.join_tables[0].get_root()
        code = self.__to_code_util__(root=root)
        return code

    def __to_code_util__(self, root: Table, from_key=None, to_key=None) -> List[str]:
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
            code += self.__to_code_util__(child.to_table, child.from_table_key, child.to_table_key)

        if root.parent:
            if root.parent.owner == root.owner:
                # TODO: Remove this error when the original code changed
                raise RuntimeError("Cannot semi join by the same owner")
            agg = root.get_aggregate_columns()
            rendered = template.render(left_table=root.parent, right_table=root,
                                       aggregate=agg, left=from_key, right=to_key,
                                       should_aggregate=len(agg) > 0, should_join=True)

            code += rendered.split("\n")

        else:
            group_by = self.__get_group_by__()
            select = self.__get_select__()
            selections = []
            is_group_by = False
            if group_by:

                selections = [i.normalized for i in group_by.identifier_list]
                is_group_by = True
            elif select:
                selections = [i.normalized for i in select.identifier_list]
            else:
                raise SyntaxError("SQL Statement should have select statement")

            columns = root.get_columns_after_aggregate()
            new_selections = self.__preprocess_selection__(selections=selections, columns=columns)
            agg = [Column(name=s, column_type=TypeEnum.int) for s in new_selections]

            rendered = template.render(left_table=root.parent, right_table=root,
                                       aggregate=agg, left=from_key, right=to_key,
                                       should_aggregate=True, should_join=False,
                                       reveal_table=root, should_reveal=True, is_group_by=is_group_by)
            code += rendered.split("\n")

        return code

    def __preprocess_selection__(self, columns: List[Column], selections: List[str]) -> List[str]:
        new_selections = []
        for selection in selections:
            for column in columns:
                if column.name == selection:
                    new_selections.append(column.name)
                else:
                    for rc in column.related_columns:
                        if rc.name == selection:
                            new_selections.append(column.name)

        return new_selections
