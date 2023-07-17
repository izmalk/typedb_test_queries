# from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions
#
# with TypeDB.core_client("0.0.0.0:1729") as client:
#
#     for method_name in dir(client):
#         if callable:
#             (getattr(client, method_name))
#             print(method_name)


from typedb.client import TypeDB, TypeDBOptions


def print_methods(obj, nesting_level=0):
    for method_name in dir(obj):
        if not method_name.startswith('_'):
            method = getattr(obj, method_name)
            if callable(method):
                indent = nesting_level * "-"
                print(f"{indent}{method_name}")
                print_methods(method, nesting_level + 1)


with TypeDB.core_client("0.0.0.0:1729") as client:
    print_methods(client)
    # for db in client.databases().all():
    #     print(db.name())

    # object_methods = [method_name for method_name in dir(client) if callable(getattr(client, method_name))]
    # print(object_methods)

# from typedb.client import TypeDB, TypeDBOptions
#
#
# def print_methods(obj, nesting_level=0):
#     for method_name in dir(obj):
#         if not method_name.startswith('_'):
#             method = getattr(obj, method_name)
#             if callable(method):
#                 indent = nesting_level * "-"
#                 print(f"{indent}{method_name}")
#                 print_methods(method, nesting_level + 1)
#
#
# def print_nested_methods(obj, nesting_level=0):
#     print_methods(obj, nesting_level)
#     for method_name in dir(obj):
#         if not method_name.startswith('_'):
#             method = getattr(obj, method_name)
#             if not callable(method):
#                 print_nested_methods(method, nesting_level + 1)
#
#
# with TypeDB.core_client("0.0.0.0:1729") as client:
#     print_nested_methods(client)