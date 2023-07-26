import sqlite3

conn = sqlite3.connect('tasktracker.db')
db = conn.cursor()

def consult_users_table():
    db.execute('''SELECT *
                FROM users''')

    print(db.fetchall())


def consult_tasks_table():
    db.execute('''SELECT *
                FROM tasks''')

    print(db.fetchall())