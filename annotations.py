from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions, Annotations
from datetime import datetime

print("Test annotations")

print("Connecting to the server")
with TypeDB.core_client("localhost:1729") as client:  # Connect to TypeDB server
    print("Connecting to the `iam` database")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as session
        print("\nRequest #1: Get query — with annotations")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has full-name $n;"
            response = transaction.query().match(typeql_read_query)  # Executing query
            k = 0
            for item in response:  # Iterating through response
                k += 1  # Counter
                print("User #" + str(k) + ": " + item.get("n").as_attribute().get_value())
                user_key_attribute_types = item.get("u").as_entity().get_type().as_thing_type().as_remote(transaction).\
                    get_owns(annotations={Annotations.KEY})
                for key in user_key_attribute_types:  # Default schema has no results
                    print(key.get_label())
            print("Users found:", k)  # Print number of results

print("Closing app")
