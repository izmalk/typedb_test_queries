from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions

client = TypeDB.core_client("0.0.0.0:1729")

# create database
client.databases().create("test-db")

# get database schema
print(client.databases().get("test-db").schema())

# get all databases
for db in client.databases().all():
    print(db.name())

# check if database exists
if client.databases().contains("test-db"):
    print("OK (1/2)")

# delete database
client.databases().get("test-db").delete()

# check if database exists
if not client.databases().contains("test-db"):
    print("OK (2/2)")

session = client.session("iam", SessionType.DATA)

transaction = session.transaction(TransactionType.READ)

typeql_read_query = "match $p isa person, has full-name $p-fname; $o isa object, has path $o-path;" \
                    "$a isa action, has action-name 'modify_file'; $ac(accessed-object: $o, valid-action: $a) isa access;" \
                    "$pe(permitted-subject: $p, permitted-access: $ac) isa permission; $p-fname = 'Kevin Morrison';" \
                    "get $o-path; sort $o-path asc;"
iterator = transaction.query().match(typeql_read_query)
i = 0
for item in iterator:  # Iterating through results
    i += 1
    print("File #" + str(i) + ":", item.get("o-path").as_attribute().get_value())

transaction.close()

session.close()

client.close()

print("Total results", i)
