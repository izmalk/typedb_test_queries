from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions
from datetime import datetime

print("IAM Test App")

print("Connecting to the server")
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    print("Connecting to the `iam` database")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as Session
        print("Request #1: User listing")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has full-name $n;"
            iterator = transaction.query().match(typeql_read_query)  # Executing query
            k = 0
            for item in iterator:  # Iterating through results
                k += 1  # Counter
                print("User #" + str(k) + ": " + item.get("n").get_value())
            print("Users found:", k)  # Print number of results

        print("\nRequest #2: Add a new file and a view access to it")
        filepath = "logs/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log"
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write

            typeql_insert_query = "insert $f isa file, has path '" + filepath + "';"
            print("Inserting file:", filepath)
            insert_response_file = transaction.query().insert(typeql_insert_query)  # runs the query
            for item in insert_response_file:
                a = item.map()
                print("Returned concepts: ", a)
                print("Returned value: ", item.get("_0").get_value())

            # print(insert_response_file.get())
            typeql_insert_query = "match $f isa file, has path '" + filepath + "'; " \
                                  "$vav isa action, has action-name 'view_file'; " \
                                  "insert ($vav, $f) isa access;"
            print("Adding view access to the file")
            insert_response_relation = transaction.query().insert(typeql_insert_query)  # runs the query
            for item in insert_response_relation:
                b = item.map()
                print(b)
            # print(insert_response_relation.get())
            transaction.commit()  # commits the transaction

        print("\nRequest #3: Delete the newly added file and a view access to it")
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write

            typeql_delete_query = "match $f isa file, has path '" + filepath + "'; " \
                                  "$vav isa action, has action-name 'view_file'; " \
                                  "$ac ($vav, $f) isa access; " \
                                  "delete $ac isa access;"
            print("Deleting view access to the file")
            delete_response_relation = transaction.query().delete(typeql_delete_query)  # runs the query
            x = delete_response_relation.get()
            print(x)

            typeql_delete_query = "match $f isa file, has path '" + filepath + "'; delete $f isa file;"
            print("Deleting file:", filepath)
            delete_response_file = transaction.query().delete(typeql_delete_query)  # runs the query
            # print(delete_response_file.get())
            y = delete_response_file.get()
            print(y)
            print("Closing app")
            transaction.commit()  # commits the transaction