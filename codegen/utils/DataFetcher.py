"""
This will fetch database data from database
"""
from typing import List
from copy import deepcopy
from codegen.table.python_free_connex_table import PythonFreeConnexTable
from codegen.database import DatabaseDriver
from os import path


class DataFetcher:
    def __init__(self, db_driver: DatabaseDriver):
        """
        Construct a db fetcher instance. It requires to have a db driver input,
        in order to fetch different files

        :param db_driver: A db_driver, can be postgres_db_driver
        """
        self.db_driver = db_driver

    def store_data(self, output_dir: str, tables: List[PythonFreeConnexTable], should_write=True) -> List[
        PythonFreeConnexTable]:
        """
        Perform a select on all tables and stored output data into the [output_dir].
        Will also return a new list of tables which has the dat_path and data_size set.

        :type should_write: object
        :param output_dir: Output dir
        :param tables: List of tables
        :return:
        """
        new_tables = deepcopy(tables)
        for i, table in enumerate(tables):
            if len(table.annotations) > 0:
                annotations = ""
                for index, annotation in enumerate(table.annotations):
                    annotations += f"{annotation} as {table.get_annotation_name(index)}"
                    if index < len(table.annotations) - 1:
                        annotations += ","

                sql = f"select *, {annotations} from {table._table_name};"
            else:
                sql = f"select * from {table._table_name};"
            output_path = path.join(output_dir, table.variable_table_name) + '.tbl'
            size = 0
            if should_write:
                size = self.db_driver.execute_save(sql=sql, output_filename=output_path)
            new_tables[i].data_paths = [output_path]
            new_tables[i].data_sizes = [size]
        return new_tables
