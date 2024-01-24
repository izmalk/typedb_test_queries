from typedb.driver import TypeDB, SessionType, TransactionType, TypeDBOptions

with TypeDB.core_driver("127.0.0.1:1729") as client:  # Connect to TypeDB server
    with client.session("iam", SessionType.DATA) as session:
        print("\nRequest #1: Explain query — Files that Kevin Morrison has view access to (with explanation)")
        with session.transaction(TransactionType.READ, TypeDBOptions(infer=True, explain=True)) as transaction:
            typeql_read_query = "match $p isa person, has full-name $p-fname; $o isa object, has path $o-path;" \
                                "$a isa action, has name 'view_file'; $ac(object: $o, action: $a) isa access;" \
                                "$pe(subject: $p, access: $ac) isa permission; $p-fname = 'Kevin Morrison';" \
                                "get $o-path; sort $o-path asc;"
            iterator = transaction.query.get(typeql_read_query)
            i = 0
            for item in iterator:  # Iterating through results
                i += 1
                explainable_relations = item.explainables().relations()
                e = 0
                for explainable in explainable_relations:
                    e += 1
                    explain_iterator = transaction.query.explain(explainable_relations[explainable])
                    ex = 0
                    for explanation in explain_iterator:
                        ex += 1

                        print("\nRead result #:", i, ", File path:", item.get("o-path").as_attribute().get_value())
                        print("Explainable #:", e, ", Explained variable:", explainable)
                        print("Explainable object:", explainable_relations[explainable])
                        print("Explainable part of query:", explainable_relations[explainable].conjunction())
                        print("Explanation #:", ex)

                        print("\nRule: ", explanation.rule().label)
                        print("Condition: ", explanation.condition())
                        print("Conclusion: ", explanation.conclusion())
                        # print("Variables used in explanation: ", explanation.query_variables())
                        print("Variable mapping: ")
                        for var in explanation.query_variables():
                            print(f"  Query variable {var} maps to the rule variable {explanation.query_variable_mapping(var)}")
                        print("----------------------------------------------------------")
