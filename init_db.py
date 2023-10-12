import sqlite3

# Create connection to db
conn = sqlite3.connect('urls.db')

# Create db based on schema.sql
with open('schema.sql') as db_init_file:
    conn.executescript(db_init_file.read())

# Close the connection
conn.commit()
conn.close()