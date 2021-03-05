import unittest

from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table


class JoinTest(unittest.TestCase):
    def setUp(self):
        self.a_table = Table(table_name="a",
                             columns=[Column(name="name", column_type=TypeEnum.string),
                                      Column(name="id", column_type=TypeEnum.int)])
        self.b_table = Table(table_name="b", columns=[Column(name="name", column_type=TypeEnum.string),
                                                      Column(name="id", column_type=TypeEnum.int)])

    def test_simple_join(self):
        self.a_table.join(self.b_table, "id", "id")
        self.assertEqual(len(self.a_table.children), 1)



