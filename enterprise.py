from typedb.driver import TypeDB, SessionType, TransactionType, TypeDBOptions, TypeDBCredential
from datetime import datetime

print("Enterprise — IAM Test all types of queries and their response")

credentials = TypeDBCredential("admin", "password", tls_enabled=False)
# tls_root_ca_path= "/Users/vladimir/tests/cluster/2.16.1/server/conf/encryption/ext-root-ca.pem")

print("Connecting to the cluster")
with TypeDB.enterprise_driver("127.0.0.1:1729", TypeDBCredential("admin", "password", tls_enabled=False)) as client:  # Connect to TypeDB cluster
    # check if database exists
    if client.databases.contains("iam"):
        print("Database iam exists, reusing.")
    else:
        client.databases.create("iam")
        print("Database iam created.")
    print("Connecting to the `iam` database")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as session
        print("\nRequest #1: Get query — User listing")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has full-name $n; get;"
            response = transaction.query.get(typeql_read_query)  # Executing query
            print(">TypeDB responded with", type(response), '<')  # Stream of ConceptMap
            k = 0
            for item in response:  # Iterating through response
                k += 1  # Counter
                print("User #" + str(k) + ": " + item.get("n").as_attribute().get_value())
            print("Users found:", k)  # Print number of results

'''
        print("\nRequest #2: Get with aggregation query — User count")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has full-name $n; count;"
            response = transaction.query().match_aggregate(typeql_read_query)  # Executing query
            print(">TypeDB responded with", type(response), '<')  # QueryFuture of Numeric
            result = response.get().as_int()
            print("Number of users in database:", result)

        print("\nRequest #3: Get with grouping query — Files per person listing (grouped)")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $pe ($x, $y) isa permission; $x isa person, has full-name $x-n; " \
                                "$y (accessed-object: $o, valid-action: $act) isa access; $act has action-name $act-n; " \
                                "$o has path $o-fp; get $x-n, $o-fp; group $x-n;"
            response = transaction.query().match_group(typeql_read_query)  # Executing query
            print(">TypeDB responded with", type(response), '<')  # Stream of ConceptMapGroup
            g = 0
            for conceptMapGroup in response:
                g += 1
                print("Group#", g, ",", conceptMapGroup.owner().as_attribute().get_value())
                k = 0
                for item in conceptMapGroup.concept_maps():  # Iterating through response
                    k += 1  # Counter
                    print("File #" + str(k) + ": " + item.get("o-fp").as_attribute().get_value())
                print("Files found in this group:", k)  # Print number of results
            print(g, "groups found.")

        print("\nRequest #4: Get with grouping and aggregation query — Files per person (counted groups)")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $pe ($x, $y) isa permission; $x isa person, has full-name $x-n; " \
                                "$y (accessed-object: $o, valid-action: $act) isa access; $act has action-name $act-n; " \
                                "$o has path $o-fp; get $x-n, $o-fp; group $x-n; count;"
            response = transaction.query().match_group_aggregate(typeql_read_query)  # Executing query
            print(">TypeDB responded with", type(response), '<')  # Stream of NumericGroup
            g = 0
            for numericGroup in response:
                g += 1
                print("Group#", g, ", owner: ", numericGroup.owner().as_attribute().get_value())  # Print group #, owner
                print("Files found in this group:", numericGroup.numeric().as_int())  # Print count for the group
            print(g, "groups found.")

        print("\nRequest #5: Insert query — Insert a file entity and some relations")
        filepath = "logs/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log"
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write
            typeql_insert_query = "insert $f isa file, has path '" + filepath + "';"
            print("Inserting file:", filepath)
            response = transaction.query().insert(typeql_insert_query)  # runs the query
            print(">TypeDB responded with", type(response), '<')  # Stream of ConceptMap
            k = 0
            for item in response:
                k += 1
                print("Inserted file #" + str(k) + ":")
                print("Returned concepts: ", item.map())
                print("File path: ", item.get("_0").as_attribute().get_value())
            print("Files inserted:", k)

            # print(insert_response_file.get())
            typeql_insert_query = "match $f isa file, has path '" + filepath + "'; " \
                                  "$vav isa action, has action-name 'view_file'; " \
                                  "insert ($vav, $f) isa access;"
            print("Adding view access to the file")
            response = transaction.query().insert(typeql_insert_query)  # runs the query
            print(">TypeDB responded with", type(response), '<')  # Stream of ConceptMap
            k = 0
            for item in response:
                k += 1
                print("Inserted access relation #" + str(k) + ":")
                print("Returned concepts: ", item.map())
                print("Relation: ", item.get("_0").as_relation().get_iid())
            transaction.commit()  # commits the transaction

        print("\nRequest #6: Delete query — Delete the newly added file and a view access to it")
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write

            typeql_delete_query = "match $f isa file, has path '" + filepath + "'; " \
                                  "$vav isa action, has action-name 'view_file'; " \
                                  "$ac ($vav, $f) isa access; " \
                                  "delete $ac isa access;"
            print("Deleting view access to the file", filepath)
            response = transaction.query().delete(typeql_delete_query)  # runs the query
            print(">TypeDB responded with", type(response), '<')  # QueryFuture
            result = response.get()
            print("Result:", result)

            typeql_delete_query = "match $f isa file, has path '" + filepath + "'; delete $f isa file;"
            print("Deleting file:", filepath)
            response = transaction.query().delete(typeql_delete_query)  # runs the query
            print(">TypeDB responded with", type(response), '<')  # QueryFuture
            result = response.get()
            print("Result:", result)
            transaction.commit()  # commits the transaction

        print("\nRequest #7: Update query — Get with grouping and aggregation query — User listing")
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write
            typeql_update_query = "match $p isa person, has full-name 'Masako Holley', has email $email; " \
                                  "delete $p has $email; " \
                                  "insert $p has email 'masako.holley@vaticle.com';"
            print("Deleting view access to the file", filepath)
            response = transaction.query().update(typeql_update_query)  # runs the query
            print(">TypeDB responded with", type(response), '<')  # Stream of ConceptMap
            k = 0
            for item in response:
                k += 1
                print("Inserted email #" + str(k) + ":")
                print("Returned concepts: ", item.map())
                print("Email: ", item.get("_0").as_attribute().get_value())
            transaction.commit()  # commits the transaction
            print("Emails inserted:", k)

    with client.session("iam", SessionType.SCHEMA) as session:  # Access schema of the `iam` database as session
        print("\nRequest #8: Define query — Define a new entity")
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write
            typeql_define_query = "define test sub entity, owns name;"
            response = transaction.query().define(typeql_define_query)  # runs the query
            print(">TypeDB responded with", type(response), '<')  # QueryFuture
            result = response.get()
            print("Result:", result)
            transaction.commit()  # commits the transaction

        print("\nRequest #9: Undefine query — Undefine a new entity")
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write
            typeql_undefine_query = "undefine test sub entity;"
            response = transaction.query().undefine(typeql_undefine_query)  # runs the query
            print(">TypeDB responded with", type(response), '<')  # QueryFuture
            result = response.get()
            print("Result:", result)
            transaction.commit()  # commits the transaction

    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as session
        print("\nRequest #10: Explain query — Files that Kevin Morrison has view access to (with explanation)")
        typedb_options = TypeDBClusterOptions.cluster()  # Initialising a new set of options
        typedb_options.infer = True  # Enabling inference in this new set of options
        typedb_options.explain = True
        typedb_options.read_any_replica = True

        with session.transaction(TransactionType.READ, typedb_options) as transaction:  # Open transaction to read with inference
            typeql_read_query = "match $u isa user, has full-name 'Kevin Morrison'; $pe ($u, $pa) isa permission; " \
                                "$o isa object, has path $fp; $pa($o, $va) isa access; " \
                                "$va isa action, has action-name 'view_file'; get $fp; sort $fp asc;"
            iterator = transaction.query().match(typeql_read_query)
            i = 0
            for item in iterator:  # Iterating through results
                i += 1
                explainable_relations = item.explainables().relations()
                e = 0
                for explainable in explainable_relations:
                    e += 1
                    explain_iterator = transaction.query().explain(explainable_relations[explainable])
                    ex = 0
                    for explanation in explain_iterator:
                        ex += 1

                        print("\nRead result #:", i, ", File path:", item.get("fp").as_attribute().get_value())
                        print("Explainable #:", e, ", Explained variable:", explainable)
                        print("Explainable object:", explainable_relations[explainable])
                        print("Explainable part of query:", explainable_relations[explainable].conjunction())
                        print("Explanation #:", ex)

                        print("\nRule: ", explanation.rule().get_label())
                        print("Condition: ", explanation.condition())
                        print("Conclusion: ", explanation.conclusion())
                        print("Variables used in explanation: ", explanation.variable_mapping())
                        print("----------------------------------------------------------")
'''

print("Closing app")
