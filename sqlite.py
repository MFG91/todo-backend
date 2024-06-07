import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("create table data(title, entries)")

res ={}

cursor.executemany(("insert into data values (?,?,?,?, ...)", res))
connection.close()
