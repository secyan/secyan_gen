from enum import Enum


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

    @property
    def name_with_table(self):
        """
        Will return column name in following format
        Order.name
        :return:
        """
        return f"{self.table.variable_table_name}.{self.name}"


class JoinColumn:
    def __init__(self, to_table: "Table", from_table: "Table", to_table_key: str, from_table_key: str):
        self.to_table = to_table
        self.to_table_key = to_table_key
        self.from_table_key = from_table_key
        self.from_table = from_table
