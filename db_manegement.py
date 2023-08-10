import sqlite3
import time

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


opt = -1

while True:
    opt = input('\n|||Menu|||\n\n0 - Exit program\n1 - Consult users table\n2 - Consult tasks table\nWhich option do you want to execute?: ')
    
    if opt == '1':
        consult_users_table()
    elif opt == '2':
        consult_tasks_table()
    elif opt == '0':
        break

print('Closing program...')
time.sleep(2)
print('Program closed!')