from typedb.driver import TypeDB, SessionType, TransactionType

SERVER_ADDR = "127.0.0.1:1729"
DB_NAME = "sample_db"
QUERY = """match
            $u isa user, has name "Bob";
            insert
            $new-u isa user, has name "Charlie", has email "charlie@vaticle.com";
            $f($u,$new-u) isa friendship;"""

with TypeDB.core_driver(SERVER_ADDR) as driver:
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            response = transaction.query.insert(QUERY)
            i = 0
            for concept in response:
                i += 1
            if i == 1:
                transaction.commit()
                print("Inserted one new user and one relation")
            else:
                print(f"Unexpected number of inserts attempted: {i}")
                transaction.close()
