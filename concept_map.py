from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions

with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    with client.session("iam", SessionType.DATA) as session:
        print("\nRequest #1: Get a concept map — Files that Kevin Morrison has access to")
        with session.transaction(TransactionType.READ) as transaction:
            typeql_read_query = "match $p isa person, has full-name $p-fname; $o isa object, has path $o-path;" \
                                "$a isa action, has action-name 'modify_file'; " \
                                "$ac(accessed-object: $o, valid-action: $a) isa access;" \
                                "$pe(permitted-subject: $p, permitted-access: $ac) isa permission; " \
                                "$p-fname = 'Kevin Morrison';" \
                                "get $o-path; sort $o-path asc;"
            iterator = transaction.query().match(typeql_read_query)
            i = 0
            for item in iterator:  # Iterating through results
                i += 1
                print("\nResult#", i)
                print("Get:", item.get("o-path").as_attribute().get_value())
                print("Concepts:", item.concepts())
                print("Map:", item.map())
            if i == 0:
                print("\nNo results returned.")
