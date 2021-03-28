from typing import List

from sqlparse.sql import Identifier, Token

from .BaseNode import BaseNode
from ..table import Table


class FromNode(BaseNode):
    def __init__(self, tables):
        super().__init__(tables=tables)
        self.self_identify = "From"
        self.from_tables: List[Identifier] = []

    def merge(self):
        for table in self.tables:
            for i in self.identifier_list:
                if i.normalized.lower() == table.variable_table_name:
                    table.used = True
