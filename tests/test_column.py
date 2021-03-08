import unittest

from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table


class TestColumn(unittest.TestCase):
    def test_equal(self):
        column1 = Column(name="a", column_type=TypeEnum.int)
        column2 = Column(name="b", column_type=TypeEnum.int)

        table_1 = Table(columns=[column1], table_name="1")
        table_2 = Table(columns=[column2], table_name="2")

        column1 = table_1.original_column_names[0]
        column2 = table_2.original_column_names[0]

        column1.related_columns.append(column2)
        column2.related_columns.append(column1)

        self.assertTrue(column1 == column2)

