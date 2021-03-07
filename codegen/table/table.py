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
        self._column_names: List[Column] = [Column(table=self, name=c.name, column_type=c.column_type) for c in columns]

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
        if len(self.children) == 0:
            return self._column_names
        else:
            column_names = self._column_names
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

    def has_column_with_name(self, column_name: str) -> bool:
        for column in self.column_names:
            if column.name == column_name:
                return True

        return False

    def join(self, table: "Table", key_a: str, key_b: str):
        """
        Join another table
        :param key_b: key from table_b
        :param key_a: key from table_a, or self table
        :param table: another table or table b
        :return:
        """
        if not table.has_column_with_name(key_b):
            raise RuntimeError(f"Cannot find the key {key_b} in table {table}")

        if not self.has_column_with_name(key_a):
            raise RuntimeError(f"Cannot find the key {key_a} in table {self}")

        self.children.append(JoinColumn(to_table=table, to_table_key=key_a, from_table_key=key_b, from_table=self))
        table.parent = self

        return self
