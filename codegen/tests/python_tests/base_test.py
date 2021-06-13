from typing import List, Dict
from unittest import TestCase
from codegen.table.python_free_connex_table import PythonFreeConnexTable
import importlib.resources as pkg_resources
import codegen.tests.test_data as test_data


class BaseTestCase(TestCase):
    tables: List[PythonFreeConnexTable]

    def replace_paths(self, mapping: Dict[str, str]):
        for table in self.tables:
            if table.variable_table_name in mapping:
                replaced_name = mapping[table.variable_table_name]
                len_names = len(table.data_paths)
                table.data_paths = [replaced_name for i in range(len_names)]

    def generate_mapping(self) -> Dict[str, str]:
        mapping = {}

        with pkg_resources.path(test_data, "customer.tbl") as p:
            mapping['customer'] = str(p)

        with pkg_resources.path(test_data, "lineitem.tbl") as p:
            mapping['lineitem'] = str(p)

        with pkg_resources.path(test_data, "orders.tbl") as p:
            mapping['orders'] = str(p)

        with pkg_resources.path(test_data, "part.tbl") as p:
            mapping['part'] = str(p)

        with pkg_resources.path(test_data, "partsupp.tbl") as p:
            mapping['partsupp'] = str(p)

        with pkg_resources.path(test_data, "supplier.tbl") as p:
            mapping['supplier'] = str(p)

        return mapping

