from typing import List, Optional, Tuple
import sqlparse
from sqlparse.sql import Comment, Identifier, Statement, Where, Token, IdentifierList, Comparison
from .node.BaseNode import BaseNode
from .node.FromNode import FromNode
from .node.SelectNode import SelectNode
from .node.WhereNode import WhereNode
from .table.table import Table
from .table.free_connex_table import FreeConnexTable
from jinja2 import Template
from . import templates
from .node.GroupbyNode import GroupByNode
from .node.OrderByNode import OrderByNode

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


class Parser:
    def __init__(self, sql: str, tables: List[Table]):
        self.sql = sql
        self.tokens: List[Token] = sqlparse.parse(sql)[0].tokens
        self.root = BaseNode(tables=[])
        self.tables: List[Table] = tables

    @property
    def root_table(self) -> Table:
        return [t for t in self.tables if t.used][0].get_root()

    def get_output_attributes(self) -> List[str]:
        node = self.root
        while node:
            if type(node) == SelectNode:
                return [str(i) for i in node.identifier_list]
            else:
                node = node.next
        return []

    def get_non_output_attributes(self, output_attrs: List[str]) -> List[str]:
        attrs = []
        tables = [t for t in self.tables if t.used]
        for table in tables:
            for col in table.original_column_names:
                for a in output_attrs:
                    if not col.equals_name(a):
                        if col.name not in attrs:
                            attrs.append(col.name)

        return attrs


    def is_free_connex(self) -> Tuple[bool, List["Table"]]:
        root_table: FreeConnexTable = self.root_table
        height = root_table.get_height()
        output_attrs = self.get_output_attributes()
        non_output_attrs = self.get_non_output_attributes(output_attrs=output_attrs)

        return root_table.is_free_connex(output_attrs=output_attrs,
                                         non_output_attrs=non_output_attrs,
                                         height=height)

    def parse(self):
        for token in self.tokens:
            if not token.is_whitespace:
                if type(token) == Token:
                    if token.normalized == "SELECT":
                        self.__parse__select__()
                    elif token.normalized == "GROUP BY":
                        self.__parse_group_by__()
                    elif token.normalized == "FROM":
                        self.__parse_from__()
                    elif token.normalized == "ORDER BY":
                        self.__parse_order_by__()
                elif type(token) == Where:
                    token: Where
                    self.__parse_where__(token)
                elif type(token) == Identifier:
                    token: Identifier
                    self.__parse__identifier__(token)
                elif type(token) == IdentifierList:
                    token: IdentifierList
                    self.__parse__identifier_list__(token)
        cur = self.root
        while cur:
            cur.merge()
            cur = cur.next
        return self

    def to_code(self):
        code = []
        cur = self.root
        while cur:
            c = cur.to_code()
            if c:
                code += c
            cur = cur.next

        return code

    def to_file(self, file_name: str):
        template = Template(pkg_resources.read_text(templates, "template.j2"))
        with open(file_name, 'w') as f:
            lines = self.to_code()
            generated = template.render(function_lines=lines)
            f.write(generated)

    def to_output(self) -> str:
        """
        Generate code and return
        :return:
        """
        template = Template(pkg_resources.read_text(templates, "template.j2"))
        lines = self.to_code()
        generated = template.render(function_lines=lines)
        return generated

    def __parse_from__(self):
        last = self.root.get_last_node()
        last.next = FromNode(tables=self.tables)
        last.next.prev = last

    def __parse_where__(self, token: Where):
        last = self.root.get_last_node()
        comparison_list: List[Comparison] = []
        for t in token.tokens:
            if type(t) == Comparison:
                comparison_list.append(t)
        last.next = WhereNode(comparison_list=comparison_list, tables=self.tables)
        last.next.prev = last

    def __parse_group_by__(self):
        last = self.root.get_last_node()
        last.next = GroupByNode(tables=self.tables)
        last.next.prev = last

    def __parse_order_by__(self):
        last = self.root.get_last_node()
        last.next = OrderByNode(tables=self.tables)
        last.next.prev = last

    def __parse__select__(self):
        last = self.root.get_last_node()
        last.next = SelectNode(tables=self.tables)
        last.next.prev = last

    def __parse__identifier__(self, token: Identifier):
        last = self.root.get_last_node()
        last.set_identifier_list([token])

    def __parse__identifier_list__(self, token: IdentifierList):
        last = self.root.get_last_node()
        tokens = [t for t in token.get_identifiers()]
        last.set_identifier_list(tokens)
