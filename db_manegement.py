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


opt = input('1 - Consult users table\n2 - Consult tasks table\nWhich option do you want to execute?: ')

if opt == '1':
    consult_users_table()
elif opt == '2':
    consult_tasks_table()
else:
    print('Invalid option!')