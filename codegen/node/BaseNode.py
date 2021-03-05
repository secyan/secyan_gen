from typing import List, Optional
from sqlparse.sql import Identifier, IdentifierList, Token


class BaseNode:

    def __init__(self):
        self.self_identify = "Base"
        self.child: Optional["BaseNode"] = None
        self.identifier_list: List["BaseNode"] = []

    def print_graph(self):
        cur = self

        while cur:
            print(f"{cur.self_identify} - {cur.identifier_list}")
            print("|")
            cur = cur.child

    def merge(self):
        pass

    def to_code(self) -> List[str]:
        """
        Generate code
        :return:
        """
        pass

    def get_last_node(self) -> "BaseNode":
        cur = self

        while cur.child:
            cur = cur.child

        return cur
