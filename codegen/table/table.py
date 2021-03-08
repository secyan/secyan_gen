from copy import deepcopy
from enum import Enum
from typing import List

from .column import Column, JoinColumn


class Table:

    def __init__(self, table_name: str, columns: List[Column]):
        """
        Create a table with columns
        :param table_name: table name
        :param columns: list of columns
        """

        self._table_name = table_name
        self.parent: "Table" = None
        self.children: List["JoinColumn"] = []
        self.original_column_names: List[Column] = [Column(table=self, name=c.name, column_type=c.column_type) for c in columns]

    def __str__(self):
        return f"<Table: {self._table_name} />"

    @property
    def variable_table_name(self):
        """
        Get a table's variable name. Used in codegen
        :return:
        """
        return self._table_name.lower()

    @property
    def column_names(self):
        """
        Will return list of column names. However, this will not apply aggregate function.
        :return:
        """
        if len(self.children) == 0:
            return self.original_column_names
        else:
            column_names = [c for c in self.original_column_names]
            for join_column in self.children:
                for column_name in join_column.to_table.column_names:
                    column_names.append(column_name)

            # merge join fields
            for join_column in self.children:
                for i, column_name in enumerate(column_names):
                    if column_name.name == join_column.to_table_key and column_name.table == join_column.to_table:
                        del column_names[i]
                        break

            return column_names

    def get_aggregate_columns(self) -> List[Column]:
        agg = []
        if self.parent and self.parent.parent:
            parent_columns = self.parent.column_names
            parent_parent_columns = self.parent.parent.original_column_names
            diff = []
            for pc in parent_columns:
                if pc in parent_parent_columns:
                    diff.append(pc)

            for d in diff:
                if d in self.column_names:
                    agg.append(d)

        elif self.parent and not self.parent.parent:
            parent_columns = self.parent.original_column_names
            for c in parent_columns:
                for cr in c.related_columns:
                    if cr == c:
                        agg.append(cr)

        return agg

    def has_column_with_name(self, column_name: str) -> bool:
        for column in self.column_names:
            if column.name == column_name:
                return True

        return False

    def join(self, to_table: "Table", from_table_key: str, to_table_key: str):
        """
        Join another table
        :param to_table_key: key from table_b
        :param from_table_key: key from table_a, or self table
        :param to_table: another table or table b
        :return:
        """
        if not to_table.has_column_with_name(to_table_key):
            raise RuntimeError(f"Cannot find the key {to_table_key} in table {to_table}")

        if not self.has_column_with_name(from_table_key):
            raise RuntimeError(f"Cannot find the key {from_table_key} in table {self}")

        join_column = JoinColumn(to_table=to_table, to_table_key=to_table_key,
                                 from_table_key=from_table_key, from_table=self)
        self.children.append(join_column)
        to_table.parent = self
        to_column = join_column.to_table_join_column
        from_column = join_column.from_table_join_column

        to_column.related_columns.append(from_column)
        from_column.related_columns.append(to_column)

        return self
