from typing import List
from sqlparse.tokens import Comparison
from codegen.node.cpp_nodes import FreeConnexWhereNode
from codegen.table import Table, Column, TypeEnum
from codegen.table.python_free_connex_table import PythonFreeConnexTable


class FreeConnexWherePythonNode(FreeConnexWhereNode):

    def to_code(self, root, *args, **kwargs):
        if root:
            assert type(root) == PythonFreeConnexTable
            code = self.__to_code_util__(root=root)

    def __to_code_util__(self, root: PythonFreeConnexTable, from_key=None, to_key=None):
        """
               Do a post-order tree Traversal to generate code
               :param root: current table
               :param from_key: join key. From table's column name
               :param to_key: join key. To table's column name
               :return: list of generated code
               """
        code = []
        for child in root.children:
            code += self.__to_code_util__(child.to_table, child.from_table_key, child.to_table_key)

        should_aggregate = False

        if root.parent:
            # If has parent, then do the join.
            # If the number of agg is greater than 0, then do the aggregation

            # if root.parent.owner == root.owner:
            #     # TODO: Remove this error when the original code changed
            #     raise RuntimeError("Cannot semi join by the same owner")
            agg = root.get_aggregate_columns()
            agg = self.remove_duplicates(agg)
            should_aggregate = len(agg) > 0

            root.parent.relation.semi_join_attr(root.relation, from_key, to_key)
            if should_aggregate:
                root.relation.aggregate_names([a.name for a in agg])

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

            should_aggregate = len(agg) > 0
            if should_aggregate:
                root.relation.aggregate_names([a.name for a in agg])
