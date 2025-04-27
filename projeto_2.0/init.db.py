import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as r:
    connection.executescript(r.read())

cor = connection.cursor()

cor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", ('First Post', 'Content for the first post') )

cor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", ('Second Post', 'Content for the second post') )

connection.commit()

connection.close()