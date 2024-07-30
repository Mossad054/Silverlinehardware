import sqlite3

# Connect to the existing database
old_db = sqlite3.connect('database.sqlite3')
new_db = sqlite3.connect('silverline2.sqlite3')

# Get the schema from the old database
schema = ""
for line in old_db.iterdump():
    if line.startswith("CREATE TABLE"):
        schema += f"{line}\n"

# Execute the schema in the new database
new_db.executescript(schema)

# Close the connections
old_db.close()
new_db.close()

print("Schema copied successfully to new_database.sqlite3")
