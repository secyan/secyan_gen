"""
Fetch table schema
"""
from typing import Dict, List

from ..database.baseDB import DatabaseDriver
from ..table import FreeConnexTable, Table
from ..table.column import Column, TypeEnum


class SchemaFetcher:

    def __init__(self, db_driver: DatabaseDriver):
        self.db_driver = db_driver

    def get_schema(self) -> List[FreeConnexTable]:
        """
        Get list of tables from the database. Will return a list of tables but without data_paths and data_sizes set

        :return:
        """

        sql = """SELECT tables.table_name, columns.column_name, columns.data_type
                    FROM information_schema.tables AS tables
                        JOIN information_schema.columns AS columns
                            ON tables.table_name = columns.table_name
                    WHERE tables.table_type = 'BASE TABLE'
                    AND tables.table_schema NOT IN
                    ('pg_catalog', 'information_schema');"""

        data = self.db_driver.execute(sql=sql)
        column_map: Dict[str, List[Column]] = {}
        for table_name, column_name, column_type in data:
            data_type = TypeEnum.from_database_type(column_type)
            if table_name not in column_map:
                column_map[table_name] = [Column(name=column_name, column_type=data_type)]
            else:
                col_list = column_map[table_name]
                col_list.append(Column(name=column_name, column_type=data_type))

        tables = []

        for table_name, columns in column_map.items():
            table = FreeConnexTable(table_name=table_name, columns=columns, data_sizes=[100], data_paths=[f""],
                                    annotations=[])
            tables.append(table)

        return tables
