from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions
from datetime import datetime

print("IAM Test all types of queries and their response")

print("Connecting to the server")
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    print("Prepare a database")
    db_name = "date-test"
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
        print("This is the schema now: ")
        print(session.database().schema())
    with client.session(db_name, SessionType.DATA) as session:  # Open a data session
        with session.transaction(TransactionType.WRITE) as transaction:
            tql_data_insert = "insert $p isa person, has name 'Peter', has join-date 2022-11-21T10:23:13;"
            date = datetime.strptime("2022-05-12T11:47:54.11", "%Y-%m-%dT%H:%M:%S.%f")
            date_string = date.strftime("%Y-%m-%dT%H:%M:%S.%f")
            print("The second date:" + date_string)
            tql_data_insert += " $p isa person, has name 'Ivan', has join-date " + date_string + ";"
            transaction.query().insert(tql_data_insert)
            transaction.commit()

    with client.session(db_name, SessionType.DATA) as session:  # Open a data session
        with session.transaction(TransactionType.READ) as transaction:
            tql_data_read = "match $p isa person, has $a;"
            response = transaction.query().match(tql_data_read)
            k = 0
            for item in response:  # Iterating through response
                k += 1  # Counter
                result = item.get("a").as_attribute().get_value()
                print("Result #" + str(k) + ":", result, "Type:", type(result))
