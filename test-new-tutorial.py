from typedb.driver import *
db_name = "social_network"

with TypeDB.core_driver("localhost:1729") as driver:
    if not driver.databases.contains(db_name):
        driver.databases.create(db_name)
        if driver.databases.contains(db_name):
            print("Created new DB!")
        else:
            print("Failed to create a DB!")
    else:
        print("Reusing an existing DB!")
    with driver.session(db_name, SessionType.DATA) as session:
        ## session is open
        pass
    ## session is closed
## driver is closed