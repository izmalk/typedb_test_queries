from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions

with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    with client.session("iam", SessionType.DATA) as session:
        print("\nRequest #1: Explain query — Files that Kevin Morrison has view access to (without explanation)")
        # typedb_options = TypeDBOptions.core()  # Initialising a new set of options
        # typedb_options.infer = True  # Enabling inference in this new set of options
        # typedb_options.explain = True
        with session.transaction(TransactionType.READ) as transaction:
            typeql_read_query = "match $p isa person, has full-name $p-fname; $o isa object, has path $o-path;" \
                                "$a isa action, has action-name 'view_file'; $ac(accessed-object: $o, valid-action: $a) isa access;" \
                                "$pe(permitted-subject: $p, permitted-access: $ac) isa permission; $p-fname = 'Kevin Morrison';" \
                                "get $o-path; sort $o-path asc;"
            iterator = transaction.query().match(typeql_read_query)
            i = 0
            print(iterator)
            for item in iterator:  # Iterating through results
                i += 1
                print("\nRead result #:", i, ", File path:", item.get("o-path").as_attribute().get_value())

                explainable_relations = item.explainables().relations()
                e = 0
                for explainable in explainable_relations:
                    e += 1
                    explain_iterator = transaction.query().explain(explainable_relations[explainable])
                    ex = 0
                    for explanation in explain_iterator:
                        ex += 1


                        print("Explainable #:", e, ", Explained variable:", explainable)
                        print("Explainable object:", explainable_relations[explainable])
                        print("Explainable part of query:", explainable_relations[explainable].conjunction())
                        print("Explanation #:", ex)

                        print("\nRule: ", explanation.rule().get_label())
                        print("Condition: ", explanation.condition())
                        print("Conclusion: ", explanation.conclusion())
                        print("Variables used in explanation: ", explanation.variable_mapping())
                        print("----------------------------------------------------------")