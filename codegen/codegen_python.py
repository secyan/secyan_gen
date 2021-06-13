import datetime
from typing import List

from secyan_python.utils import DateTime

from .codegen_fromDB import CodeGenDB
from .database.baseDB import DatabaseDriver
from .node.python_nodes import SelectNodePython
from .table.python_free_connex_table import PythonFreeConnexTable


def cpp_datetime_to_python_datetime(date: DateTime):
    """
    Helper function. Which will convert c++ custom struct DateTime to python DateTime

    :param date:
    :return:
    """
    return datetime.datetime(year=date.year, month=date.month, day=date.day)


class CodeGenPython(CodeGenDB):
    def __init__(self, sql: str, db_driver: DatabaseDriver, tables: List[PythonFreeConnexTable], annotation_name: str):
        """
        Code Gen for python code. This code will generate a python code instead of c++ code.

        :param sql: SQL Query
        :param db_driver: DB Driver
        :param tables: List of tables
        """
        super().__init__(sql, db_driver, tables, annotation_name=annotation_name)

    def __parse_select__(self):
        last = self.root.get_last_node()
        last.next = SelectNodePython(tables=self.tables, annotation_name=self.annotation_name)
        last.next.prev = last

    def __to_code__(self) -> List[PythonFreeConnexTable]:
        relations = []
        cur = self.root
        while cur:
            c = cur.to_code(root=self.root_table)
            if type(cur) == SelectNodePython:
                relations = c
            cur = cur.next

        return relations

    def to_output(self, function_name="run_Demo",
                  output_table_name: str = "", limit_size=10, *args, **kwargs) -> List[List[str]]:
        """
        This method will output the result from the SQL statement.
        If not specify the output_table_name, the root table in the join tree will be used.
        The return result will be a python list, and follows the format:
        - First row is the header
        - Rest of the rows will be the actual contents. It will be the type of string, number, and python datetime object

        :param function_name: function name
        :param output_table_name: Which table will be used to generate output results
        :param limit_size: Number of rows of the result
        :param args:
        :param kwargs:
        :return:
        """

        relations = self.__to_code__()

        if len(output_table_name) > 0:
            for relation in relations:
                if relation.variable_table_name == output_table_name.lower():
                    results = relation.relation.return_print_results(limit_size=limit_size,
                                                                     show_zero_annoted_tuple=True)
                    return self.__convert_c_to_python__(results)
        else:
            # noinspection PyTypeChecker
            root: PythonFreeConnexTable = self.root_table
            results = root.relation.return_print_results(limit_size=limit_size, show_zero_annoted_tuple=True)
            return self.__convert_c_to_python__(results)

        return []

    def __convert_c_to_python__(self, results):
        """
        Helper method to convert c++ result to python.

        :param results:
        :return:
        """

        ret = []
        # Do the c++ DateTime to python DateTime.
        # If do not do the conversion, the code will break.
        # Since Python Queue expect a python object
        for row in results:
            r = []
            for col in row:
                if isinstance(col, DateTime):
                    try:
                        r.append(cpp_datetime_to_python_datetime(col))
                    except Exception:
                        r.append(None)
                else:
                    r.append(col)
            ret.append(r)
        return ret
