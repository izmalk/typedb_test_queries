from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions


def print_methods(obj, nesting_level=0):
    for index, method_name in enumerate(dir(obj)):
        # print(method_name)
        if not (method_name.startswith('_') or method_name == 'stub'):
            method = getattr(obj, method_name)
            if callable(method):
                indent = nesting_level * "-"
                print(f"{indent} {index} {method_name}")
                print_methods(method, nesting_level + 1)


with TypeDB.core_client("0.0.0.0:1729", parallelisation=1) as client: # https://typedb.com/docs/clients/2.x/python/python-api-ref.html#_instantiating_a_typedb_core_client
    # for db in client.databases().all(): print(db.name())
    # if client.databases().contains(client.databases().all()[1].name()): print(client.databases().all()[1].name() + " found!")
    # print_methods(client.databases())
    print("------")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as session
        print("\nCheck value methods")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $f isa object, has size-kb $sk; ?sm = $sk / 1024;"
            response = transaction.query().match(typeql_read_query)  # Executing query
            # print(">TypeDB responded with", type(response), '<')  # Stream of ConceptMap
            k = 0
            for item in response:  # Iterating through response
                k += 1  # Counter
                # z = item.get("sm")
                y = item.get("sk")
                # print_methods(z.as_value())
                # print("---")
                print_methods(y)
                print("Value #" + str(k) + ": " + str(item.get("sk").to_json()))
            print("Values found:", k)  # Print number of results

    # with client.session("iam", SessionType.DATA):
    #
    #
    # print_methods(client)
