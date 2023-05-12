from typedb.client import TypeDB, SessionType

print('Connecting')
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server

    if not client.databases().contains("test-delete"):
        client.databases().create("test-delete")
        if client.databases().contains("test-delete"):
            print("Created")
        else:
            print("Not created")
    else:
        print("Reusing existing DB")

    with client.session("test-delete", SessionType.SCHEMA) as session:
        print("Get me name")
        print(session.database().name())
        print("Get me schema")
        print(session.database().schema())
        print(session.database().delete())

    if not client.databases().contains("test-delete"):
        print("Deleted")
