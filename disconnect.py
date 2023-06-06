from typedb.client import TypeDB, SessionType, TransactionType
from datetime import datetime
import time

print("Testing session timeout")

counter = 0

print("Connecting to the server")
client = TypeDB.core_client("0.0.0.0:1729")
print("Prepare a database")
db_name = "timeout-test"
if client.databases().contains(db_name):
    client.databases().get(db_name).delete()
client.databases().create(db_name)
print("Connecting to the database to load schema")
session = client.session(db_name, SessionType.SCHEMA)
transaction = session.transaction(TransactionType.WRITE)

tql_schema_insert = "define"
tql_schema_insert += " person sub entity, owns name, owns join-date;"
tql_schema_insert += " name sub attribute, value string;"
tql_schema_insert += " join-date sub attribute, value datetime;"
transaction.query().define(tql_schema_insert)
transaction.commit()
session.close()
print("Schema loaded")

session = client.session(db_name, SessionType.DATA)
transaction = session.transaction(TransactionType.WRITE)
tql_data_insert = "insert"
tql_data_insert += " $p isa person,"
tql_data_insert += " has name '" + str(counter) + "',"
timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
tql_data_insert += " has join-date " + timestamp + ";"
transaction.query().insert(tql_data_insert)
transaction.commit()
print("Initial data inserted:", timestamp)

transaction = session.transaction(TransactionType.WRITE)
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
    if counter == 3:
        counter = counter / 0
transaction.commit()

print("Counter:", counter)

print("Exiting")
