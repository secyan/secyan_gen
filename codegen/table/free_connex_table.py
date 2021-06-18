from .table import Table, CharacterEnum, JoinColumn
from .column import Column
from typing import List, Tuple


class FreeConnexTable(Table):
    def __init__(self, table_name: str, columns: List[Column], data_sizes: List[float], data_paths: List[str],
                 owner: CharacterEnum = None):
        super().__init__(table_name, columns, data_sizes=data_sizes, owner=owner, data_paths=data_paths)

    @staticmethod
    def load_from_json(json_content: dict) -> "FreeConnexTable":
        """
        Construct a table from json content
        :param json_content:
        :return:
        """
        assert "table_name" in json_content
        assert "columns" in json_content

        columns = [Column.load_column_from_json(c) for c in json_content['columns']]
        return FreeConnexTable(table_name=json_content["table_name"], columns=columns,
                               owner=CharacterEnum[json_content['owner']] if "owner" in json_content else None,
                               data_sizes=json_content['data_sizes'], data_paths=json_content['data_paths'])

    def swap(self):
        # TODO: implement this function
        if self.parent and len(self.children) > 0:
            tmp_parent_join_column: JoinColumn = self.parent.children[-1]
            tmp_parent_join_column.swap()

            tmp_join_column: JoinColumn = self.children[-1]
            tmp_table = tmp_join_column.to_table

            tmp_join_column.swap()

            self.children = self.children[:-1] + [tmp_parent_join_column]
            self.parent = tmp_table

            # tmp.parent = self.parent.parent
            # tmp.children = self.children[1:]
            # tmp.children = tmp.children[:-1]

    def get_highest_with_attr(self, output_attr: str, height: int) -> Tuple["Table", int]:
        """
        Get the highest table contains attr
        :param output_attr:
        :param height:
        :return: Table, height
        """

        if self.has_column_with_name_without_aggregation(output_attr):
            return self, height

        temp = []
        for child in self.children:
            table: "Table" = child.to_table
            t, h = table.get_highest_with_attr(output_attr, height - 1)
            temp.append((t, h))

        topmost = temp[0][1] if len(temp) > 0 else 0
        result_table = temp[0][0] if len(temp) > 0 else None

        for t, h in temp:
            if h > topmost:
                topmost = h
                result_table = t

        return result_table, topmost

    def is_free_connex(self, output_attrs: List[str], non_output_attrs: List[str], height) -> Tuple[
        bool, List["Table"]]:
        """
        If free connex table. Only call this method on root node
        :param output_attrs: list of output attributes str
        :param non_output_attrs: list of non-output attributes str
        :param height: height of the tree
        :return: true if is free connex join tree, otherwise, false
        """
        assert self.parent is None

        output_attr_tables: List["Table"] = []
        non_output_attr_tables: List["Table"] = []

        not_qualified_tables = []

        for attr in output_attrs:
            table, _ = self.get_highest_with_attr(attr, height=height)
            if table:
                output_attr_tables.append(table)

        for attr in non_output_attrs:
            table, _ = self.get_highest_with_attr(attr, height=height)
            if table:
                non_output_attr_tables.append(table)

        for ot in output_attr_tables:
            for nt in non_output_attr_tables:
                if ot and ot.parent == nt:
                    not_qualified_tables.append(ot)

        not_qualified_tables = list(set(not_qualified_tables))

        return len(not_qualified_tables) == 0, not_qualified_tables

    def is_cycle(self, visited: List["FreeConnexTable"] = None) -> bool:
        """
        Whether this join tree has a cycle

        :param visited: a list of tables visited
        :return: True if has a cycle
        """

        if visited is None:
            visited = []

        if self in visited:
            return True
        for c in self.children:
            c: JoinColumn
            table: "FreeConnexTable" = c.to_table
            is_cycle = table.is_cycle(visited=visited)
            if is_cycle:
                return True

        return False
