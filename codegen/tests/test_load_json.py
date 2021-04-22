import unittest

from codegen.table.column import TypeEnum
from codegen.table.table import Table, CharacterEnum


class LoadJsonTest(unittest.TestCase):
    def test_simple_load_table1(self):
        json_content = {
            "table_name": "A",
            "owner": "client",
            "data_sizes": [100],
            "columns": [
                {
                    "column_type": "int",
                    "name": "a"
                },
                {
                    "column_type": "int",
                    "name": "b"
                },
                {
                    "column_type": "string",
                    "name": "c"
                }
            ]
        }

        table = Table.load_from_json(json_content=json_content)
        self.assertEqual("a", table.variable_table_name)
        self.assertEqual(CharacterEnum.client, table.owner)

        self.assertEqual(table.original_column_names[0].column_type, TypeEnum.int)
        self.assertEqual(table.original_column_names[0].name, "a")

        self.assertEqual(table.original_column_names[1].column_type, TypeEnum.int)
        self.assertEqual(table.original_column_names[1].name, "b")

        self.assertEqual(table.original_column_names[2].column_type, TypeEnum.string)
        self.assertEqual(table.original_column_names[2].name, "c")



