"""
This will fetch database data from database
"""
from typing import List

from codegen.table.python_free_connex_table import PythonFreeConnexTable
from codegen.database import DatabaseDriver


class DataFetcher:
    def __init__(self, db_driver: DatabaseDriver):
        """
        Construct a db fetcher instance. It requires to have a db driver input,
        in order to fetch different files

        :param db_driver: A db_driver, can be postgres_db_driver
        """
        self.db_driver = db_driver

    def store_data(self, output_dir: str, tables: List[PythonFreeConnexTable]) -> List[PythonFreeConnexTable]:
        """
        Perform a select on all tables and stored output data into the [output_dir].
        Will also return a new list of tables which has the dat_path and data_size set.

        :param output_dir: Output dir
        :param tables: List of tables
        :return:
        """
