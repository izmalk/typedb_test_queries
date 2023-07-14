from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions
from datetime import datetime


def get_all_methods(obj, parent=''):
    methods = []
    for attr_name in dir(obj):
        if attr_name.startswith('__'):
            continue
        try:
            attr = getattr(obj, attr_name)
        except AttributeError:
            continue
        if callable(attr):
            full_method_name = f"{parent}.{attr_name}" if parent else attr_name
            print(full_method_name)
            methods.append(full_method_name)
        if hasattr(attr, '__dict__'):
            methods.extend(get_all_methods(attr, parent=f"{parent}.{attr_name}" if parent else attr_name))
    return methods


print("IAM Test all types of queries and their response")

print("Connecting to the server")
with TypeDB.core_client("localhost:1729") as client:  # Connect to TypeDB server
    print("Connecting to the `iam` database")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as session
        print("\nRequest #1: Get query — User listing")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has full-name $n;"
            response = transaction.query().match(typeql_read_query)  # Executing query
            # print(">TypeDB responded with", type(response), '<')  # Stream of ConceptMap
            k = 0
            for item in response:  # Iterating through response
                k += 1  # Counter
                print("User #" + str(k) + ": " + item.get("n").as_attribute().get_value())
                # Get a list of all methods and attributes of the object
                # methods = [method_name for method_name in dir(item.get("n")) if callable(getattr(item.get("n"),
                #                                                                                  method_name))]
                #
                # # Print the list of methods
                # for method_name in methods:
                #     print(method_name)

                get_all_methods(item.get("n"))
            print("Users found:", k)  # Print number of results
