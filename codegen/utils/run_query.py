from queue import Queue

from secyan_python.constant import E_role
from secyan_python.utils import init_global_party

from codegen.codegen_python import CodeGenPython


def run_query(sql, role: E_role, queue: Queue, tables, driver, annotation_name, num_of_rows):
    try:
        init_global_party(address="0.0.0.0", port=7766, role=role)
        parser = CodeGenPython(db_driver=driver, sql=sql, tables=tables, annotation_name=annotation_name)
        parser.parse()
        output = parser.to_output(limit_size=num_of_rows)
        graph = parser.root_table.to_json_graph(
            output_attrs=parser.get_output_attributes()) if parser.root_table else {}

        is_free_connex, error_tables = parser.is_free_connex()
        error_tables = [e.variable_table_name for e in error_tables]
        queue.put((False, output, graph, is_free_connex, error_tables))

    except Exception as e:
        queue.put((True, e))