from typedb.client import TypeDB, SessionType

print('Here is the IAM database schema:')
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    with client.session("iam", SessionType.SCHEMA) as session:
        print("session.database():", session.database(), ">Response type was:", type(session.database()), "<")
        print("session.database().name():", session.database().name(), ">Response type was:", type(session.database().name()), "<")
        print("First 100 symbols of session.database().schema():\n" + session.database().schema()[:100])
        session.close()

    if not client.databases().contains("test-delete"):
        client.databases().create("test-delete")
        if client.databases().contains("test-delete"):
            print("Created a new DB to try the delete.")
        else:
            print("WARNING! Not created: DB not found after the API call to create it.")
    else:
        print("WARNING! Pre-existing DB found: reusing existing DB!")

    with client.session("test-delete", SessionType.SCHEMA) as session2:
        print("Session opened")
        print("session2.database().name():", session2.database().name())
        # print("session2.database().schema():", session2.database().schema())
        print("session2.database().delete():", session2.database().delete())
        print("session2.database().name():", session2.database().name())

    if not client.databases().contains("test-delete"):
        print("Deleted successfully.")
