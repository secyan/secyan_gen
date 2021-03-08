from typing import List

from jinja2 import Template
from sqlparse.sql import Identifier

from .BaseNode import BaseNode
from ..table.table import Table


class SelectNode(BaseNode):
    def __init__(self, tables: List[Table]):
        """
        Select statement
        :param tables: a list of tables used to generate code
        """
        super().__init__()
        self.self_identify = "Selection"
        self.from_tables: List[Identifier] = []
        self.tables: List[Table] = tables

    def merge(self):
        """
        Merge data from from node
        :return:
        """
        if self.next and self.next.self_identify == "From":
            self.from_tables = self.next.identifier_list
            self.next = self.next.next
        else:
            print("aaa")

    def to_code(self) -> List[str]:
        output = []
        for f in self.from_tables:
            tb_name = f.normalized.lower()
            table: Table = None
            for t in self.tables:
                if t.variable_table_name == tb_name:
                    table = t

            template = Template(self.open_template_file("select.template.j2"))
            owner = "SERVER"
            attr_names = [c.name for c in table.column_names]
            attr_types = [c.column_type.value for c in table.column_names]
            rendered = template.render(attr_names=attr_names, attr_types=attr_types,
                                       owner=owner, from_table=f, table=table, table_name=tb_name)

            output += rendered.split("\n")

        return output
