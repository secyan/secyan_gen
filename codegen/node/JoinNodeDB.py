from typing import List

from jinja2 import Template

from .BaseNode import BaseNode
from .GroupbyNode import GroupByNode
from .JoinNode import JoinNode, JoinData
from .SelectNode import SelectNode
from ..table.column import Column, TypeEnum
from ..table.table import Table
from sqlparse.sql import Identifier


class JoinNodeDB(JoinNode):
    """
    Join Node used for DB
    """

    def __init__(self, join_list: List[JoinData], tables: List[Table]):
        super().__init__(join_list, tables)

    def merge(self):
        """
        Perform join
        :return:
        """
    pass

