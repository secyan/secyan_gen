from typing import List

from sqlparse.sql import Identifier

from .BaseNode import BaseNode


class FromNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.self_identify = "From"
        self.from_tables: List[Identifier] = []
