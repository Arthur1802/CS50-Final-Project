import sqlite3

conn = sqlite3.connect('tasktracker.db')

db = conn.cursor()

db.execute('''
           CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, hased_password TEXT, dateBirth DATE)
           ''')

db.execute('''
           CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, description TEXT, dateCreated DATE, dateStart DATE, dateEnd DATE, status DATE)
           ''')

conn.close()