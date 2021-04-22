from typing import Dict, List, Optional, Tuple, Callable
import psycopg2
import json

from .baseDB import DatabaseDriver
from .dbplan import DBPlan
from ..node.FreeConnexJoinNode import FreeConnexJoinNode
from ..node.JoinNode import JoinData
from ..table.table import Table
from ..utils import CreateDBHelper


class PostgresDBDriver(DatabaseDriver):
    """
    Postgres DB driver
    """

    def __init__(self, database_name: str, user: str, password: str, host: str, port: str, tables: List[Table]):
        super().__init__(tables)
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def init(self, data: str):
        """
        Create a database with pre-defined table structure.

        :param data: A sql statement which can create tables.
        :return:
        """

        util = CreateDBHelper(tables=self.tables, database_name=self.database_name)
        conn = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        print("Drop db")
        cursor.execute(util.drop_db())

        print("Create DB")
        cursor.execute(util.create_db())
        conn.close()

        conn = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                port=self.port, database=self.database_name)
        cursor = conn.cursor()

        print("Create Tables")
        for statement in data.split(";"):
            if "create" in statement.lower():
                cursor.execute(statement)

        conn.commit()

    def get_query_plan(self, sql: str) -> "PostgresDBPlan":
        try:
            conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host,
                                    port=self.port)
            cur = conn.cursor()
            print("Connect to the database")
        except Exception as e:
            raise RuntimeError("Cannot connect to the database. Please check config.")
        cur.execute(f"""EXPLAIN (FORMAT JSON) {sql}""")
        data = cur.fetchone()
        return PostgresDBPlan.from_json(data[0][0]['Plan'], tables=self.tables)


class PostgresDBPlan(DBPlan):
    """
    Postgres DB Plan. This object should be construct by the JSON query plan
    """

    node_type: str
    parallel_aware: bool
    startup_cost: float
    total_cost: float
    plan_rows: int
    plan_width: int
    plans: List["PostgresDBPlan"]
    hash_cond: str
    relation_name: str

    def __init__(self, node_type: str, parallel_aware: bool, startup_cost: float, total_cost: float, plan_rows: int,
                 plan_width: int, plans: List["PostgresDBPlan"], tables: List[Table], hash_cond: str,
                 relation_name: str) -> None:
        super().__init__(tables)
        self.node_type = node_type
        self.parallel_aware = parallel_aware
        self.startup_cost = startup_cost
        self.total_cost = total_cost
        self.plan_rows = plan_rows
        self.plan_width = plan_width
        self.plans = plans
        self.hash_cond = hash_cond
        self.relation_name = relation_name

    def __str__(self):
        return f"<PostgresDBPlan: {self.node_type} />"

    def perform_select_from(self) -> List[Table]:
        """
        Get a list of tables used in the select statement from the query plan

        :return: A list of tables used in the select statement
        """

        return self.__perform__select_from__util__()

    def __perform__select_from__util__(self) -> List[Table]:
        results = []
        for plan in self.plans:
            rs = plan.__perform__select_from__util__()
            results += rs

        if self.is_scan:
            found_table = None
            for table in self.tables:
                if table.variable_table_name == self.relation_name.lower():
                    found_table = table

            assert found_table is not None
            return [found_table]

        return results

    def perform_join(self, is_free_connex_table: Callable[[], Tuple[bool, List[Table]]]):
        join_list: List[JoinData] = []
        self.__join__util__(join_list=join_list)
        # Use Free Connex Join Node to join tables
        node = FreeConnexJoinNode(join_list=join_list, tables=self.tables, is_free_connex_table=is_free_connex_table)
        node.merge()

    def __parse_join_key__(self, content: str) -> Tuple[str, str]:
        """
        Return left join key and right join key
        :param content:
        :return:
        """
        try:
            new_content = content.replace("(", "")
            new_content = new_content.replace(")", "")
            left = new_content.split("=")[0]
            right = new_content.split("=")[1]

            return left.split('.')[1].replace(" ", ""), right.split(".")[1].replace(" ", "")
        except Exception:
            raise SyntaxError("Cannot parse this join condition")

    def __join__util__(self, join_list: List[JoinData], depth=0) -> Optional[Tuple[Table, int]]:
        """
        Join helper function.
        :return: Founded table and its depth
        """

        left_table: Optional[Table] = None
        right_table: Optional[Table] = None
        left_depth = 0
        right_depth = 0

        for i, plan in enumerate(self.plans):
            if i == 1:
                left_table, left_depth = plan.__join__util__(depth=depth + 1, join_list=join_list)
            else:
                right_table, right_depth = plan.__join__util__(depth=depth + 1, join_list=join_list)

        if self.is_join:
            # If the current node is a join node

            if left_table and right_table:
                left_table.used_in_join = True
                right_table.used_in_join = True
                ret_table = None

                if "AND" in self.hash_cond:
                    # If the plan returns a multiple join conditions. For example a join b and a join c.
                    conditions = self.hash_cond.split("AND")
                    for cond in conditions:
                        right_key, left_key = self.__parse_join_key__(cond)
                        # ret_table = self.__perform_join_util__(left=left_table, right=right_table, left_key=left_key,
                        #                                        right_key=right_key,
                        #                                        left_depth=left_depth, right_depth=right_depth)

                        join_list.append(JoinData(left_key=left_key, right_key=right_key))
                else:
                    right_key, left_key = self.__parse_join_key__(self.hash_cond)
                    # ret_table = self.__perform_join_util__(left=left_table, right=right_table, left_key=left_key,
                    #                                        right_key=right_key,
                    #                                        left_depth=left_depth, right_depth=right_depth)
                    join_list.append(JoinData(left_key=left_key, right_key=right_key))
                return right_table, depth

        elif self.is_scan:
            found_table = None
            for table in self.tables:
                if table.variable_table_name == self.relation_name.lower():
                    found_table = table

            assert found_table is not None

            return found_table, depth

        elif left_table:
            return left_table, left_depth

        elif right_table:
            return right_table, right_depth

    def __perform_join_util__(self, left: Table, right: Table, left_key: str, right_key: str, left_depth,
                              right_depth):
        if left_depth < right_depth:
            left.join(right, from_table_key=left_key, to_table_key=right_key)
            return left
        else:
            right.join(left, from_table_key=right_key, to_table_key=left_key)
            return right

    @property
    def is_join(self) -> bool:
        """
        If current plan is a join plan
        :return:
        """
        return 'join' in self.node_type.lower()

    @property
    def is_scan(self) -> bool:
        """
        If current plan is scan plan
        :return:
        """
        return 'scan' in self.node_type.lower()

    @staticmethod
    def from_json(obj, tables: List["Table"]) -> 'PostgresDBPlan':
        """
        Load database plan from json scr
        :param obj:
        :param tables:
        :return:
        """
        assert type(obj) == dict
        node_type = obj.get("Node Type")
        parallel_aware = obj.get("Parallel Aware")
        startup_cost = obj.get("Startup Cost")
        total_cost = obj.get("Total Cost")
        plan_rows = obj.get("Plan Rows")
        plan_width = obj.get("Plan Width")
        hash_cond = obj.get("Hash Cond")
        relaton_name = obj.get("Relation Name")
        plans = [PostgresDBPlan.from_json(p, tables=tables) for p in obj.get("Plans", [])]
        return PostgresDBPlan(node_type, parallel_aware, startup_cost, total_cost, plan_rows, plan_width, plans,
                              tables=tables, hash_cond=hash_cond, relation_name=relaton_name)
