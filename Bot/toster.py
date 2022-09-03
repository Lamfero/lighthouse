import sqlite3 as sql

con = sql.connect("db.sqlite3")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS `users` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)")
con.commit()