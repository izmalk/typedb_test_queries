from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions

print('Here is the IAM database schema:')
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    with client.session("iam", SessionType.SCHEMA) as session:
        print(session.database().schema())

