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
            tql_schema_insert += " person sub entity, owns name, owns join-date, plays friendship:friend;"
            tql_schema_insert += " name sub attribute, value string;"
            tql_schema_insert += " join-date sub attribute, value datetime;"
            tql_schema_insert += " friendship sub relation, relates friend, relates friends, plays friendship:friends;"
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
            tql_data_insert += " $r(friend:$p) isa friendship;"
            transaction.query().insert(tql_data_insert)
            transaction.commit()
            print("Initial data inserted:", timestamp)

        try:
            with session.transaction(TransactionType.WRITE) as transaction:
                while counter < 17:
                    counter += 1
                    tql_data_match = "match $t isa thing; get $t; count;"
                    survey = transaction.query().match_aggregate(tql_data_match)
                    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    print(timestamp, "Counting the number of instances in the DB:", survey.get().as_int())
                    tql_data_match_insert = "match"
                    tql_data_match_insert += " $p isa person;"
                    tql_data_match_insert += " $or isa friendship;"
                    tql_data_match_insert += "insert"
                    tql_data_match_insert += " $np isa person,"
                    tql_data_match_insert += " has name '" + str(counter) + "',"
                    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    tql_data_match_insert += " has join-date " + timestamp + ";"
                    tql_data_match_insert += "$or(friend:$p, friend:$np) isa friendship;"
                    tql_data_match_insert += "$r(friend:$p, friend:$np) isa friendship;"
                    print("timestamp:", timestamp, "Sending query#", counter)
                    response = transaction.query().insert(tql_data_match_insert)
                    # for r in response:
                    #     for item in r.concepts():
                    #         print(item.to_json())

                transaction.commit()
        except Exception as e:
            print("Exception detected:", e)
            print("Counter:", counter)
        finally:
            print("Exiting")
