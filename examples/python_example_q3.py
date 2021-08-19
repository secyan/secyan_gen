"""
This is a pure python example without using codegen.
The query this example represents is the Query 3 in the Tpch repo
"""


from multiprocessing import Queue, Process
import importlib.resources as pkg_resources
import codegen.tests.test_data as test_data
from codegen.codegen_python import cpp_datetime_to_python_datetime
from secyan_python import Relation, RelationInfo, AnnotInfo, Party
from secyan_python.constant import DataType, E_role
from secyan_python.utils import init_global_party, DateTime


sizes = [
    [150, 450, 1500, 4950, 15000],
    [1500, 4500, 15000, 49500, 150000],
    [6005, 17973, 60175, 198344, 595215],
    [200, 600, 2000, 6600, 20000],
    [10, 30, 100, 330, 1000],
    [800, 2400, 8000, 26400, 80000]
]

mapping = {
    "customer": 0,
    "orders": 1,
    "lineitem": 2,
    "part": 3,
    "supplier": 4,
    "partsupp": 5
}


def get_filename(name: str):
    with pkg_resources.path(test_data, name) as p:
        return str(p)


def get_sizes(name: str, size_index: int) -> int:
    return sizes[mapping[name]][size_index]


def q3(size_index: int):
    customer_ri = RelationInfo(owner=E_role.CLIENT,
                               is_public=False,
                               attr_names=["c_custkey", "c_name", "c_address", "c_nationkey", "c_phone", "c_acctbal",
                                           "c_mktsegment", "c_comment"],
                               attr_types=[DataType.INT, DataType.STRING, DataType.STRING, DataType.STRING,
                                           DataType.STRING, DataType.DECIMAL,
                                           DataType.STRING, DataType.STRING],
                               num_rows=get_sizes("customer", size_index=size_index), sorted=False)

    customer_ai = AnnotInfo(is_boolean=True, known_by_owner=True)
    customer = Relation(relation_info=customer_ri, annot_info=customer_ai)
    file_path = get_filename(name="customer.tbl")
    customer.load_data(file_path, "q3_annot")

    orders_ri = RelationInfo(owner=E_role.SERVER,
                             is_public=False,
                             attr_names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate",
                                         "o_orderpriority", "o_clerk",
                                         "o_shippriority", "o_comment", "c_name", "c_address", "c_nationkey", "c_phone",
                                         "c_acctbal",
                                         "c_mktsegment", "c_comment", "l_partkey", "l_suppkey", "l_linenumber",
                                         "l_quantity", "l_extendedprice",
                                         "l_discount", "l_tax", "l_returnflag", "l_linestatus", "l_shipdate",
                                         "l_commitdate", "l_receiptdate",
                                         "l_shippinstruct", "l_shipmode", "l_comment"],
                             attr_types=[DataType.INT, DataType.INT, DataType.STRING, DataType.STRING, DataType.DATE,
                                         DataType.STRING,
                                         DataType.STRING, DataType.INT, DataType.STRING, DataType.STRING,
                                         DataType.STRING, DataType.STRING,
                                         DataType.STRING, DataType.DECIMAL, DataType.STRING, DataType.STRING,
                                         DataType.INT, DataType.INT,
                                         DataType.INT, DataType.DECIMAL, DataType.DECIMAL, DataType.DECIMAL,
                                         DataType.DECIMAL,
                                         DataType.STRING, DataType.STRING, DataType.DATE, DataType.DATE, DataType.DATE,
                                         DataType.STRING,
                                         DataType.STRING, DataType.STRING],
                             num_rows=get_sizes("orders", size_index=size_index), sorted=False)

    orders_ai = AnnotInfo(is_boolean=True, known_by_owner=True)
    orders = Relation(relation_info=orders_ri, annot_info=orders_ai)
    file_path = get_filename(name="orders.tbl")
    orders.load_data(file_path, "q3_annot")

    lineitem_ri = RelationInfo(owner=E_role.CLIENT,
                               is_public=False,
                               attr_names=["l_orderkey", "l_partkey", "l_suppkey", "l_linenumber", "l_quantity",
                                           "l_extendedprice", "l_discount",
                                           "l_tax", "l_returnflag", "l_linestatus", "l_shipdate", "l_commitdate",
                                           "l_receiptdate", "l_shippinstruct",
                                           "l_shipmode", "l_comment"],
                               attr_types=[DataType.INT, DataType.INT, DataType.INT, DataType.INT, DataType.DECIMAL,
                                           DataType.DECIMAL,
                                           DataType.DECIMAL, DataType.DECIMAL, DataType.STRING, DataType.STRING,
                                           DataType.DATE, DataType.DATE,
                                           DataType.DATE, DataType.STRING, DataType.STRING, DataType.STRING],
                               num_rows=get_sizes("lineitem", size_index=size_index), sorted=False)

    lineitem_ai = AnnotInfo(is_boolean=False, known_by_owner=True)
    lineitem = Relation(relation_info=lineitem_ri, annot_info=lineitem_ai)
    file_path = get_filename(name="lineitem.tbl")
    lineitem.load_data(file_path, "q3_annot")

    customer.aggregate("c_custkey")
    orders.semi_join_attr(customer, "o_custkey", "c_custkey")

    lineitem.aggregate("l_orderkey")
    orders.semi_join_attr(lineitem, "o_orderkey", "l_orderkey")

    orders.aggregate_names(["o_orderkey", "o_orderdate", "o_shippriority"])
    orders.reveal_annot_to_owner()

    results = orders.return_print_results(limit_size=10, show_zero_annoted_tuple=True)
    return results


def run_example(query_func, role: E_role, size_index, queue: Queue):
    init_global_party(address="0.0.0.0", port=7766, role=role)
    result = query_func(size_index)
    ret = []

    for row in result:
        r = []
        for col in row:
            if type(col) == DateTime:
                r.append(cpp_datetime_to_python_datetime(col))
            else:
                r.append(col)
        ret.append(r)

    queue.put(ret)


if __name__ == '__main__':
    client_queue = Queue()
    server_queue = Queue()

    print("Start Client")
    client = Process(target=run_example, args=(q3, E_role.CLIENT, 0, client_queue))

    print("Start as server")
    server = Process(target=run_example, args=(q3, E_role.SERVER, 0, server_queue))

    client.start()
    server.start()

    client.join()
    server.join()

    print(client_queue.get())
    print(server_queue.get())
