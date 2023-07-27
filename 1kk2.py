from typedb.client import TypeDB, SessionType, TransactionType

print("Insert 1 million")

print("Connecting to the server")
with TypeDB.core_client("localhost:1729") as client:  # Connect to TypeDB server
    print("Connecting to the `bulkdb` database")
    with client.session("bulkdb", SessionType.DATA) as session:  # Access data in the `1kk` database as session
        print("\nRequest #1: Insert bulkdb")
        for k in range(1, 11):
            with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write
                query = "insert\n"
                for i in range(1, 1_00_001):
                    i = i + ((k-1) * 100_000)
                    full_name = f"Employee{i}"
                    email = f"employee{i}@example.com"
                    employee = f"e{i}"
                    query += "$e" + employee + " isa employee, has full-name ' " + full_name + "', has email '" + email + "';\n"
                    if i % 10000 == 0:
                        response = transaction.query().insert(query)  # Executing batch insert query
                        query = "insert\n"
                        print(f'{i:_}', "inserted")
                if len(query) > 10:  # Just in case anything left in the query variable
                    response = transaction.query().insert(query)  # Executing final insert query
                print("Batch #" + str(k) + " committing...")
                try:
                    transaction.commit()  # Commit. Takes a long time to commit so many inserted objects
                    print("Successfully committed.")
                except Exception as error:
                    print("An error occurred:", error)

print("Closing app")
