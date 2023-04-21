from typedb.client import TypeDB, SessionType
import time

print('Here is the IAM database schema:')
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    with client.session("iam", SessionType.SCHEMA) as session:
        print(session.database().schema())
        print(session.database().name())

    if not client.databases().contains("test-delete"):
        client.databases().create("test-delete")
        if client.databases().contains("test-delete"):
            print("Created")
        else:
            print("Not created")
    else:
        print("Reusing existing DB")

    with client.session("test-delete", SessionType.SCHEMA) as session:
        print(session.database().schema())
        print(session.database().name())
        print(session.database().delete())

    if not client.databases().contains("test-delete"):
        print("Deleted")
