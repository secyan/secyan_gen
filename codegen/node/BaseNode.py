from typing import List, Optional, Union

from sqlparse.sql import Identifier, Token, Function

from ..table.table import Table

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from . import templates


class BaseNode:
    # Prev statement
    prev: Optional["BaseNode"]

    # next statement
    next: Optional["BaseNode"]

    # Sub query
    child: Optional["BaseNode"]

    def __init__(self, tables: List[Table]):
        """
        Base SQL node object.
        """
        self.self_identify = "Base"
        self.prev: Optional["BaseNode"] = None
        self.child: Optional["BaseNode"] = None
        self.next: Optional["BaseNode"] = None
        self._identifier_list: List[Identifier] = []
        self.tables = tables

    @property
    def identifier_list(self):
        return self._identifier_list

    def set_identifier_list(self, value):
        self._identifier_list = value

    def print_graph(self):
        """
        Print SQL tree Graph
        :return:
        """
        cur = self

        while cur:
            print(f"{cur.self_identify} - {cur.identifier_list}")
            print("|")
            cur = cur.next

    def merge(self):
        """
        Merge data with other nodes
        :return:
        """
        pass

    def to_code(self, root) -> List[str]:
        """
        Generate code
        :return:
        """
        pass

    def get_last_node(self) -> "BaseNode":
        """
        Get last node in this tree structure
        :return:
        """
        cur = self

        while cur.next:
            cur = cur.next

        return cur

    def open_template_file(self, path: str):
        """
        Open jinja template file
        :param path: Jinja template file path
        :return:
        """
        template = pkg_resources.read_text(templates, path)
        return template

    def find_table_by_identifier_or_function(self, identifier: Union[Function, Identifier]) -> Table:
        if type(identifier) != Token and len(identifier.tokens) > 1:
            identifier: Function
            for token in identifier.tokens:
                table = self.find_table_by_identifier_or_function(token)
                if table:
                    return table

        if type(identifier) == Identifier:
            for table in self.tables:
                if table.has_column_with_name(identifier.normalized):
                    return table

    def find_table_by_table_name(self, identifier: Identifier):
        tb_name = identifier.normalized.lower()
        for table in self.tables:
            if tb_name == table.variable_table_name:
                return table
