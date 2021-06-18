from enum import Enum
from typing import List
from secyan_python.constant import E_role, DataType


class TypeEnum(Enum):
    """
    Column type
    """
    int = "INT"
    string = "STRING"
    decimal = "DECIMAL"
    date = "DATE"

    @staticmethod
    def from_database_type(db_type: str) -> "TypeEnum":
        """
        Return a typeenum from database type. This will convert Postgres DB type into a type enum

        :param self:
        :param db_type:
        :return:
        """
        if db_type.lower() == "integer":
            return TypeEnum.int
        elif db_type.lower() == "text":
            return TypeEnum.string
        elif db_type.lower() == "real":
            return TypeEnum.decimal
        elif db_type.lower() == 'date':
            return TypeEnum.date

    @property
    def data_type(self) -> DataType:
        """
        Based on the current value, return the datatype.
        Note that datatype is from secyan c++ code.

        :return:
        """

        if self == TypeEnum.int:
            return DataType.INT
        elif self == TypeEnum.decimal:
            return DataType.DECIMAL
        elif self == TypeEnum.string:
            return DataType.STRING
        elif self == TypeEnum.date:
            return DataType.DATE
        else:
            raise RuntimeError("Cannot find corresponding type")


class Column:
    def __init__(self, name: str, column_type: TypeEnum, table=None):
        """
        Create a column
        :param name: Column name
        :param column_type: Column type
        :param table: Target table
        """
        self.name: str = name
        self.column_type: TypeEnum = column_type
        self.table: "Table" = table
        self.related_columns: List["Column"] = []

    @staticmethod
    def load_column_from_json(json_content: dict) -> "Column":
        """
        Load column from json data
        :param json_content:
        :return:
        """
        assert type(json_content) == dict
        assert "column_type" in json_content
        assert "name" in json_content
        return Column(name=json_content["name"], column_type=TypeEnum[json_content['column_type'].lower()])

    def to_json(self):
        return {
            "name": self.name,
            "column_type": self.column_type.value
        }

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

    def equals_name(self, column_name: str) -> bool:
        if self.name == column_name:
            return True

        for column in self.related_columns:
            if column.name == column_name:
                return True

        return False

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
            if column.equals_name(self.to_table_key):
                return column

    @property
    def from_table_join_column(self) -> Column:
        """
        Get column from from_table with from_table_key
        :return:
        """
        for column in self.from_table.column_names:
            if column.equals_name(self.from_table_key):
                return column

    def swap(self):
        tmp = self.to_table
        tmp_key = self.to_table_key

        self.to_table = self.from_table
        self.from_table = tmp

        self.to_table_key = self.from_table_key
        self.from_table_key = tmp_key
