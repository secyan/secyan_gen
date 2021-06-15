from typing import List, Optional, Union

from sqlparse.sql import Identifier, Token, Function
from codegen.table.table import Table

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from codegen.node import templates


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
        # This will not include keywords such as sum, count
        self.built_in_keywords = ["*", "+", "-", "/", "(",
                                  ")", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    @property
    def identifier_list(self):
        """
        A list of identifiers. Identifier could be l_orderkey, s_orderkey.
        :return:
        """
        return self._identifier_list

    def set_identifier_list(self, value: List[Identifier]):
        """
        Set the identifier list equals to the value.
        :param value:
        :return:
        """
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
        Merge data with other nodes.

        For example, a join node will perform join.
        :return:
        """
        pass

    def to_code(self, root: "Table", *args, **kwargs) -> List[str]:
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
        """
        Use identifier to find the table.

        Function: something like sum(1 - price)
        Identifier: l_orderkey
        :param identifier:
        :return:
        """
        if isinstance(identifier, Token) is False and len(identifier.tokens) > 1:
            identifier: Function
            for token in identifier.tokens:
                table = self.find_table_by_identifier_or_function(token)
                if table:
                    return table

        if isinstance(identifier, Identifier) or isinstance(identifier, Token):
            for table in self.tables:
                if table.has_column_with_name(identifier.normalized):
                    return table

    def find_table_by_table_name(self, identifier: Identifier) -> Table:
        """
        Find table by its table name.
        :param identifier:
        :return:
        """
        tb_name = identifier.normalized.lower()
        for table in self.tables:
            if tb_name == table.variable_table_name:
                return table

    def find_table_by_column_name(self, identifier: str) -> Table:
        for table in self.tables:
            if table.has_column_with_name(identifier):
                return table

    def get_list_of_identifiers(self, identifier: Identifier) -> List[str]:
        """
        Will Get a list of identifiers.
        For example a sql statement like sum(1 - l_discount * l_number) will return [sum, l_discount, l_number]

        :param identifier:
        :return:
        """

        if type(identifier) == Token:
            if identifier.normalized.lower() not in self.built_in_keywords and str(identifier) != " ":
                return [identifier.normalized.lower()]
            else:
                return []

        li = []
        for token in identifier.tokens:
            li += self.get_list_of_identifiers(token)

        return li
