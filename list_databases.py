from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions

with TypeDB.core_client("0.0.0.0:1729") as client:
    all_db = client.databases().all()
    for db in all_db:
        print(db.name())
