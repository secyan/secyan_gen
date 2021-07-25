from os import getenv
from secyan_python.constant import E_role
from codegen.database.postgresDB import PostgresDBPlan, PostgresDBDriver
from multiprocessing import Process, Queue
from codegen.utils.DataFetcher import DataFetcher
from codegen.utils.SchemaFetcher import SchemaFetcher
from codegen.utils.run_query import run_query

if __name__ == '__main__':
    # Get table configurations
    password = getenv('password')
    user = getenv('user')
    database = getenv("database")
    host = getenv("host")
    port = getenv("port")
    output_dir = "../data_dir"
    num_of_rows = 100
    sql = "select * from customer"
    annotation_name = ""

    driver = PostgresDBDriver(password=password,
                              user=user,
                              database_name=database,
                              host=host,
                              port=port,
                              tables=[])

    schema_fetcher = SchemaFetcher(db_driver=driver)
    print("Getting schema")
    tables = schema_fetcher.get_schema()
    data_fetcher = DataFetcher(db_driver=driver)
    print("Fetching data")
    tables = data_fetcher.store_data(output_dir=output_dir, tables=tables)
    print("Running query")

    client_queue = Queue()
    server_queue = Queue()

    client = Process(target=run_query,
                     args=(sql, E_role.CLIENT, client_queue, tables, driver, annotation_name, num_of_rows))

    server = Process(target=run_query,
                     args=(sql, E_role.SERVER, server_queue, tables, driver, annotation_name, num_of_rows))

    client.start()
    server.start()

    client.join()
    server.join()

    # data is in the index 1
    client_result = client_queue.get()
    server_result = server_queue.get()

    print(client_result[1])
    print(server_result[1])
