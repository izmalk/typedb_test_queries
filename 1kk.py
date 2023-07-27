from typedb.client import TypeDB, SessionType, TransactionType

print("Insert 1 million")

print("Connecting to the server")
with TypeDB.core_client("localhost:1729") as client:  # Connect to TypeDB server
    print("Connecting to the `1kk` database")
    with client.session("1kk", SessionType.DATA) as session:  # Access data in the `1kk` database as session
        print("\nRequest #1: Insert 1kk employees")
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write
            query = "insert\n"
            for i in range(1, 1_00_001):
                s = str(i)
                query += "$e" + s + " isa employee, has full-name 'bob" + s + "', has email 'bob" + s + "@vaticle.com';\n"

            response = transaction.query().insert(query)  # Executing query
            transaction.commit()

print("Closing app")
