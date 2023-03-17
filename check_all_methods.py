from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions

with TypeDB.core_client("0.0.0.0:1729") as client:

    for method_name in dir(client):
        if callable:
            (getattr(client, method_name))
            print(method_name)

    # object_methods = [method_name for method_name in dir(client) if callable(getattr(client, method_name))]
    # print(object_methods)
