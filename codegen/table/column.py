from enum import Enum
from typing import List


class TypeEnum(Enum):
    """
    Column type
    """
    int = "INT"
    string = "STRING"


class Column:
    def __init__(self, name: str, column_type: TypeEnum, table=None):
        """
        Create a column
        :param name: Column name
        :param column_type: Column type
        """
        self.name: str = name
        self.column_type: TypeEnum = column_type
        self.table: "Table" = table
        self.related_columns: List["Column"] = []

    @property
    def name_with_table(self):
        """
        Will return column name in following format
        Order.name
        :return:
        """
        return f"{self.table.variable_table_name}.{self.name}"

    def __eq__(self, other: "Column"):
        if other.table == self.table and other.name == self.name:
            return True
        columns = [c for c in self.related_columns if c.table != self.table]
        for column in columns:
            if column.name == other.name and column.table == other.table:
                return True

    def __str__(self):
        return f"<Column: {self.name} />"


class JoinColumn:
    def __init__(self, to_table: "Table", from_table: "Table", to_table_key: str, from_table_key: str):
        """
        An object contains joining information
        :param to_table: Join to which table
        :param from_table: From which table
        :param to_table_key: to table's column name
        :param from_table_key: from table's column name
        """
        self.to_table = to_table
        self.to_table_key = to_table_key
        self.from_table_key = from_table_key
        self.from_table = from_table

    @property
    def to_table_join_column(self) -> Column:
        """
        Get column from to_table with to_table_key
        :return:
        """
        for column in self.to_table.column_names:
            if column.name == self.to_table_key:
                return column

    @property
    def from_table_join_column(self) -> Column:
        """
        Get column from from_table with from_table_key
        :return:
        """
        for column in self.from_table.column_names:
            if column.name == self.from_table_key:
                return column
