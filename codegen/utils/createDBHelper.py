from typing import List

from codegen.table import Table, Column, TypeEnum


class CreateDBHelper:
    def __init__(self, tables: List[Table], database_name="test"):
        self.tables = tables
        self.db_name = database_name
        self.mapping = {
            TypeEnum.int: "integer",
            TypeEnum.decimal: "real",
            TypeEnum.date: "date",
            TypeEnum.string: "text",
        }

    def create_db(self):
        return f"create database {self.db_name};"

    def drop_db(self):
        return f"drop database if exists {self.db_name}"

    def create(self):
        sql_list = ""
        for table in self.tables:
            column_sql = ""
            for i, column in enumerate(table.original_column_names):
                column_sql += self.__create__column__(column)
                if i < len(table.original_column_names) - 1:
                    column_sql += ","
                column_sql += "\n"

            sql = f"CREATE TABLE {table.variable_table_name} (\n {column_sql} );"
            sql_list += sql
        return sql_list

    def __create__column__(self, column: Column):
        name = column.name

        return f"{name} {self.mapping[column.column_type]}"
