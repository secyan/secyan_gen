from typing import List

from jinja2 import Template
from sqlparse.sql import Identifier, Function

from .BaseNode import BaseNode
from codegen.table.table import Table


class SelectNode(BaseNode):
    def __init__(self, tables: List[Table], annotation_name: str):
        """
        Select statement
        :param tables: a list of tables used to generate code
        """
        super().__init__(tables=tables)
        self.self_identify = "Selection"
        self.from_tables: List[Identifier] = []
        self.support_aggregation_functions = ["sum", "count", "avg"]
        self.annotation_name = annotation_name
        # Which aggregation function used in the sql. For example, max.
        self.used_aggregation_function: str = None

    def is_supported_function(self, identifier: str):
        for func in self.support_aggregation_functions:
            if func == identifier:
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
            is_bool = True
            for token in self.get_list_of_identifiers(identifier):
                table = self.find_table_by_column_name(token)
                if token in self.support_aggregation_functions:
                    is_bool = False
                else:
                    if table:
                        table.fields_used_in_select.append(str(token))
                        table.used_in_select = True
                        table.is_bool = is_bool

        # Merge From node data
        if self.next and self.next.self_identify == "From":
            self.from_tables = self.next.identifier_list
            self.next.merge()
            self.next = self.next.next
        else:
            pass

    def to_code(self, root, *args, **kwargs) -> List[str]:
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
