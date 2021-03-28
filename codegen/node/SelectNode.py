from typing import List

from jinja2 import Template
from sqlparse.sql import Identifier, Function

from .BaseNode import BaseNode
from ..table.table import Table


class SelectNode(BaseNode):
    def __init__(self, tables: List[Table]):
        """
        Select statement
        :param tables: a list of tables used to generate code
        """
        super().__init__(tables=tables)
        self.self_identify = "Selection"
        self.from_tables: List[Identifier] = []
        self.support_aggregation_functions = ["sum", "count", "avg"]

    def is_function_supported(self, identifier: Identifier):
        for func in self.support_aggregation_functions:
            if func in str(identifier.normalized.lower()):
                return True
        return False

    def merge(self):
        """
        Merge data from from node
        :return:
        """
        # Merge aggregation functions
        for identifier in self.identifier_list:
            identifier: Identifier
            if type(identifier) == Function:
                if self.is_function_supported(identifier):
                    table = self.find_table_by_identifier_or_function(identifier)
                    if table:
                        table.is_bool = False
            else:
                for token in identifier.tokens:
                    if type(token) == Function:
                        if self.is_function_supported(token):
                            table = self.find_table_by_identifier_or_function(token)
                            if table:
                                table.is_bool = False

        # Merge From node data
        if self.next and self.next.self_identify == "From":
            self.from_tables = self.next.identifier_list
            self.next.merge()
            self.next = self.next.next
        else:
            pass

    def to_code(self, root) -> List[str]:
        output = []
        for i, f in enumerate(self.from_tables):
            table: Table = self.find_table_by_table_name(f)
            if not table:
                raise RuntimeError("Cannot find table with this name: " + f.normalized.lower())
            template = Template(self.open_template_file("select.template.j2"))
            owner = table.owner.value
            attr_names = [c.name for c in table.column_names]
            attr_types = [c.column_type.value for c in table.column_names]
            rendered = template.render(attr_names=attr_names, attr_types=attr_types,
                                       owner=owner, from_table=f, table=table, table_name=f.normalized.lower(),
                                       is_boolean=table.is_bool, should_init_file_path=i == 0)

            output += rendered.split("\n")

        return output
