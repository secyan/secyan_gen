from enum import Enum


class TypeEnum(Enum):
    """
    Column type
    """
    int = "INT"
    string = "STRING"


class Column:
    def __init__(self, name: str, column_type: TypeEnum):
        """
        Create a column
        :param name: Column name
        :param column_type: Column type
        """
        self.name: str = name
        self.column_type: TypeEnum = column_type


class JoinColumn:
    def __init__(self, table: "Table", key_a: str, key_b: str):
        self.table = table
        self.key_a = key_a
        self.key_b = key_b