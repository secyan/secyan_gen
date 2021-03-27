from typing import Dict, List, Optional, Tuple
import psycopg2
import json

from .baseDB import DatabaseDriver
from .dbplan import DBPlan
from ..table.table import Table


class PostgresDBDriver(DatabaseDriver):
    def __init__(self, database_name: str, user: str, password: str, host: str, port: str, tables: List[Table]):
        super().__init__(tables)
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

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

    def perform_join(self):
        self.__join__util__()

    def __parse_join_key__(self, content: str) -> Tuple[str, str]:
        """
        Return left join key and right join key
        :param content:
        :return:
        """
        try:
            content = content.replace("(", "")
            content = content.replace(")", "")
            left = content.split("=")[0]
            right = content.split("=")[1]

            return left.split('.')[1].replace(" ", ""), right.split(".")[1].replace(" ", "")
        except Exception:
            raise SyntaxError("Cannot parse this join condition")

    def __join__util__(self, depth=0):
        """
        Join helper function.
        :return:
        """

        left_table: Optional[Table] = None
        right_table: Optional[Table] = None
        left_depth = 0
        right_depth = 0

        for i, plan in enumerate(self.plans):
            if i == 0:
                left_table, left_depth = plan.__join__util__(depth=depth + 1)
            else:
                right_table, right_depth = plan.__join__util__(depth=depth + 1)

        if self.is_join:
            if left_table and right_table:
                left_table.used_in_join = True
                right_table.used_in_join = True
                ret_table = None

                if "AND" in self.hash_cond:
                    conds = self.hash_cond.split("AND")
                    for cond in conds:
                        left, right = self.__parse_join_key__(cond)
                        ret_table = self.__perform_join_util__(left=left_table, right=right_table, left_key=left,
                                                               right_key=right,
                                                               left_depth=left_depth, right_depth=right_depth)
                else:
                    left, right = self.__parse_join_key__(self.hash_cond)
                    ret_table = self.__perform_join_util__(left=left_table, right=right_table, left_key=left,
                                                           right_key=right,
                                                           left_depth=left_depth, right_depth=right_depth)
                return ret_table, depth

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
