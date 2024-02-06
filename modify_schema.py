from typedb.driver import TypeDB, SessionType, TransactionType, ValueType, Transitivity

SERVER_ADDR = "127.0.0.1:1729"
DB_NAME = "sample_db"

with TypeDB.core_driver(SERVER_ADDR) as driver:
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            tag = transaction.concepts.put_attribute_type("tag", ValueType.STRING).resolve()
            entities = transaction.concepts.get_root_entity_type().get_subtypes(transaction, Transitivity.EXPLICIT)
            for entity in entities:
                print(entity.get_label())
                if not entity.is_abstract():
                    entity.set_owns(transaction, tag).resolve()
            transaction.commit()
