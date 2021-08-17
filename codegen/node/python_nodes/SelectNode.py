from typing import List, Tuple
from secyan_python import Relation, RelationInfo, AnnotInfo
from secyan_python.constant import AggregateType
from ..cpp_nodes import SelectNode
from ...table import Table
from ...table.python_free_connex_table import PythonFreeConnexTable
import os


class SelectNodePython(SelectNode):
    def to_code(self, root, index: int = 0, should_load_data=True, *args, **kwargs) -> List[PythonFreeConnexTable]:
        """
        Generate a list of Relation

        :param should_load_data: Should call load data on the relation. This is useful for tests.
        :param index: Which size you want to use. This will use the size like table.data_sizes[index]
        and table.data_paths[index]

        :param root: Root table
        :return: A list of tuple like (Table, relation)
        """

        if index is None or type(index) != int:
            raise TypeError("Size_index must be int")

        output = []
        for i, f in enumerate(self.from_tables):
            # noinspection PyTypeChecker
            table: PythonFreeConnexTable = self.find_table_by_table_name(f)
            if type(table) != PythonFreeConnexTable:
                raise TypeError(f"Instance {table} must be a type of PythonFreeConnexTable but got type: {type(table)}")

            if not table:
                raise RuntimeError("Cannot find table with this name: " + f.normalized.lower())
            owner = table.owner.get_e_role
            attr_names = [c.name for c in table.column_names]
            attr_types = [c.column_type.data_type for c in table.column_names]

            relation_info = RelationInfo(owner=owner, is_public=False, attr_names=attr_names, attr_types=attr_types,
                                         num_rows=table.data_sizes[index], sorted=False)
            a_info = AnnotInfo(is_boolean=table.is_bool, known_by_owner=True)
            relation = Relation(relation_info=relation_info, annot_info=a_info)

            if should_load_data:
                file_path = table.data_paths[index]
                # assert type(file_path) == str
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Cannot find the file {file_path} on your disk")
                if len(table.annotations) > 0:
                    # TODO: Add multiple annotations support
                    print("Use annotation")
                    relation.load_data(table.data_paths[index], table.get_annotation_name(0))
                else:
                    relation.load_data(table.data_paths[index], self.annotation_name)

            table.load_relation(relation)

            output.append(table)

        return output
