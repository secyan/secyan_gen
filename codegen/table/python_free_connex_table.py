from . import Column
from .free_connex_table import FreeConnexTable
from secyan_python import Relation

from .table import CharacterEnum


class PythonFreeConnexTable(FreeConnexTable):
    """
    Python free connex table.
    This table is different from the traditional free connex table in following ways.

    - It inherits from the FreeConnexTable however will add support for c++ code
    - The relation is a class from c++ code and this table instance will store that class
    - It will use to run the python code directly, while the original class will generate the c++ code.
    """
    relation: Relation

    @staticmethod
    def load_from_json(json_content: dict) -> "PythonFreeConnexTable":
        """
        Construct a table from json content
        :param json_content:
        :return:
        """
        assert "table_name" in json_content
        assert "columns" in json_content
        assert "data_sizes" in json_content
        assert "data_paths" in json_content

        columns = [Column.load_column_from_json(c) for c in json_content['columns']]
        return PythonFreeConnexTable(table_name=json_content["table_name"], columns=columns,
                                     owner=CharacterEnum[json_content[
                                         'owner'].lower()] if "owner" in json_content else CharacterEnum.client,
                                     data_sizes=json_content['data_sizes'], data_paths=json_content['data_paths'])

    def load_relation(self, relation: Relation):
        """
        Load relation data and store it.

        :param relation:
        :return:
        """
        self.relation = relation
