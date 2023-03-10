from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions
from datetime import datetime

print("Explain test")

print("Connecting to the server")
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    print("Connecting to the `iam` database")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as Session
        print("\nRequest #1: Files that Kevin Morrison has view access to (with inference)")
        typedb_options = TypeDBOptions.core()  # Initialising a new set of options
        typedb_options.infer = True  # Enabling inference in this new set of options
        typedb_options.explain = True
        with session.transaction(TransactionType.READ, typedb_options) as transaction:  # Open transaction to read with inference
            typeql_read_query = "match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; " \
                                "$o isa object, has path $fp; $pa($o, $va) isa access; " \
                                "$va isa action, has action-name 'view_file'; get $fp; sort $fp asc;"
            iterator = transaction.query().match(typeql_read_query)
            i = 0
            for item in iterator:  # Iterating through results
                i += 1
                print("\nNew item:")
                explainable_relations = item.explainables().relations()
                e = 0
                for explainable in explainable_relations:
                    e += 1
                    print("New explainable:")
                    explain_iterator = transaction.query().explain(explainable_relations[explainable])
                    ex = 0
                    for explanation in explain_iterator:
                        ex += 1
                        print("New explanation:")
                        print("\nRead result #:", i)
                        print("Explainable #:", e)
                        print("Explanation #:", ex)

                        print("\nRule: ", explanation.rule().get_label())
                        print("Condition: ", explanation.condition())
                        print("Conclusion: ", explanation.conclusion())
                        print("Variables: ", explanation.variable_mapping())
                        print("----------------------------------------------------------")

