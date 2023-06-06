from typedb.client import TypeDB, SessionType, TransactionType
from datetime import datetime
import time

print("Testing transaction timeout")

counter = 0

print("Connecting to the server")
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    print("Prepare a database")
    db_name = "timeout-test"
    if client.databases().contains(db_name):
        client.databases().get(db_name).delete()
    client.databases().create(db_name)
    print("Connecting to the database to load schema")
    with client.session(db_name, SessionType.SCHEMA) as session:  # Open a schema session
        with session.transaction(TransactionType.WRITE) as transaction:
            tql_schema_insert = "define"
            tql_schema_insert += " person sub entity, owns name, owns join-date;"
            tql_schema_insert += " name sub attribute, value string;"
            tql_schema_insert += " join-date sub attribute, value datetime;"
            transaction.query().define(tql_schema_insert)
            transaction.commit()
            print("Schema loaded")

    with client.session(db_name, SessionType.DATA) as session:  # Open a schema session
        with session.transaction(TransactionType.WRITE) as transaction:
            tql_data_insert = "insert"
            tql_data_insert += " $p isa person,"
            tql_data_insert += " has name '" + str(counter) + "',"
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            tql_data_insert += " has join-date " + timestamp + ";"
            transaction.query().insert(tql_data_insert)
            transaction.commit()
            print("Initial data inserted:", timestamp)

        try:
            with session.transaction(TransactionType.WRITE) as transaction:
                while True:
                    counter += 1
                    # print("Initiating wait cycle for", counter, "minutes")
                    time.sleep(1 * 60)
                    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    print(counter, "Wait cycle over:", timestamp)
                    # tql_data_insert = "insert"
                    # tql_data_insert += " person isa entity,"
                    # tql_data_insert += " has name " + str(counter) + ","
                    # timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    # tql_data_insert += " has join-date " + timestamp + ";"
                    # transaction.query().insert(tql_data_insert)
                    # print(counter, "Data insertion complete successfully: ", timestamp)
                transaction.commit()
        except Exception as e:
            print("Exception detected:", e)
            print("Counter:", counter)
        finally:
            print("Exiting")
