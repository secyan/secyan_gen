from typing import List

from jinja2 import Template

from .BaseNode import BaseNode
from .GroupbyNode import GroupByNode
from .SelectNode import SelectNode
from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table
from sqlparse.sql import Identifier


class JoinData:
    def __init__(self, left_key: str, right_key: str):
        """
        Data object contains join info
        :param left_key: key on the left join statement
        :param right_key: key on the right join statement
        """
        self.left = left_key
        self.right = right_key


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
        self.root = None

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

    def preprocess_join_list(self):
        """
        Remove the data which is not a join condition. For example a_key = "Auto"
        :return:
        """
        filtered_list = []
        for c in self.join_list:
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
                filtered_list.append(c)

        self.join_list = filtered_list

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
                column_names = [t.name for t in table.original_column_names]

                if str(c.right) in column_names and not right_table:
                    right_table = table
                    continue

                if str(c.left) in column_names and not left_table:
                    left_table = table

            if left_table and right_table:
                right_table.join(left_table, str(c.right), str(c.left))
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

    def to_code(self, root, *args, **kwargs):
        if root:
            assert isinstance(root, Table)
            code = self.__to_code_util__(root=root)
            return code
        else:
            return ""

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

        should_aggregate = False
        should_join = False

        if root.parent:
            # If has parent, then do the join.
            # If the number of agg is greater than 0, then do the aggregation

            # if root.parent.owner == root.owner:
            #     # TODO: Remove this error when the original code changed
            #     raise RuntimeError("Cannot semi join by the same owner")
            agg = root.get_aggregate_columns()
            agg = self.remove_duplicates(agg)
            should_join = True
            should_aggregate = len(agg) > 0

            rendered = template.render(left_table=root.parent, right_table=root,
                                       aggregate=agg, left=from_key, right=to_key,
                                       should_aggregate=should_aggregate, should_join=should_join)

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

            agg = self.remove_duplicates(agg)

            should_join = False
            should_aggregate = len(agg) > 0

            rendered = template.render(left_table=root.parent, right_table=root,
                                       aggregate=agg, left=from_key, right=to_key,
                                       should_aggregate=should_aggregate, should_join=should_join,
                                       reveal_table=root, should_reveal=True, is_group_by=is_group_by)
            code += rendered.split("\n")

        return code

    def remove_duplicates(self, columns: List[Column]) -> List[Column]:
        ret_columns = []
        for c in columns:
            if c not in ret_columns:
                ret_columns.append(c)

        return ret_columns

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
