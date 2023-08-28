import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import apology, login_required, dateForm

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQL('sqlite:///tasktracker.db')

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    def deleteTask(checked, user_id):
        if not checked:
            return apology('to delete a task, you must select a task', 403)
        
        for i in checked:
            db.execute('''
                       DELETE FROM tasks
                       WHERE id = ?
                       AND user_id = ?
                       ''', i, user_id)
            
        flash('Task(s) deleted successfully')
    

    def completeTask(checked, user_id):
        if not checked:
            return apology('to complete a task, you must select a task', 403)
        
        for i in checked:
            db.execute('''
                    UPDATE tasks
                    SET status = 'COMPLETED'
                    WHERE id = ?
                    AND user_id = ?
                    ''', i, user_id)
            
        flash('Task(s) completed successfully')


    if request.method == 'POST':
        user_id = session['user_id']
        checked = request.form.getlist('checked')

        if 'deleteBtn' in request.form:
            deleteTask(checked, user_id)
        
        if 'completeBtn' in request.form:
            completeTask(checked, user_id)

        else:
            return apology('you must select a task', 403)
        
        return redirect('/')
    
    else:    
        user_id = session['user_id']

        status = 'ON GOING'

        user_tasks = db.execute('''SELECT *
                                FROM tasks
                                WHERE user_id = ?
                                AND status LIKE ?
                                ''', user_id, status)
        
        return render_template('index.html', tasks = user_tasks)


@app.route('/register', methods = ['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        birthDate = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        fBirthDate = datetime.strptime(birthDate, '%Y-%m-%d').date()

        if not name:
            return apology('must provide name', 403)
        
        if not email:
            return apology('must provide email', 403)
        
        if not password:
            return apology('must provide password', 403)
        
        if not confirmation:
            return apology('must provide confirmation', 403)
        
        if not birthDate:
            return apology('must provide birth date', 403)
        
        if password != confirmation:
            return apology('passwords must match', 403)
        
        if db.execute('SELECT * FROM users WHERE email = ?', email):
            return apology('email already exists', 403)
        
        new_session = db.execute('''
                                 INSERT INTO users (name, email, hashed_password, dateBirth)
                                 VALUES (?, ?, ?, ?)
                                 ''', name, email, generate_password_hash(password), fBirthDate)
        
        session['user_id'] = new_session

        flash(f'Welcome {name}')

        return redirect('/')
        
    else:
        return render_template('register.html')
    

@app.route('/login', methods = ['GET', 'POST'])
def login():

    session.clear()

    if request.method == 'POST':

        if not request.form.get('email'):
            return apology('must provide email', 403)

        elif not request.form.get('password'):
            return apology('must provide password', 403)

        rows = db.execute('''
                          SELECT * 
                          FROM users 
                          WHERE email = ?
                          ''', request.form.get('email'))

        if len(rows) != 1 or not check_password_hash(rows[0]['hashed_password'], request.form.get('password')):
            return apology('invalid email and/or password', 403)

        session['user_id'] = rows[0]['id']

        user_name = db.execute('''
                               SELECT name
                               FROM users
                               WHERE id = ?
                               ''', session['user_id'])
        
        flash(f"Welcome {user_name[0]['name']}!")

        return redirect('/')

    else:
        return render_template('login.html')
    

@app.route('/logout')
def logout():
    
    session.clear()

    return redirect('/')


@app.route('/addTask', methods = ['GET', 'POST'])
@login_required
def addTask():

    if request.method == 'POST':
        user_id = session['user_id']
        
        title = request.form.get('title')
        description = request.form.get('description')
        dateCreation = datetime.now().date()
        year1 = request.form.get('year1')
        month1 = request.form.get('month1')
        day1 = request.form.get('day1')
        year2 = request.form.get('year2')
        month2 = request.form.get('month2')
        day2 = request.form.get('day2')
        dateStart = dateForm(year1, month1, day1) if year1 != None and month1 != None and day1 != None else None
        dateEnd = dateForm(year2, month2, day2) if year2 != None and month2 != None and day2 != None else None
        fDateStart = datetime.strptime(dateStart, '%Y-%m-%d').date() if dateStart != None else None
        fDateEnd = datetime.strptime(dateEnd, '%Y-%m-%d').date() if dateEnd != None else None
        status = 'ON GOING'

        if not title:
            return apology('must provide title', 403)
        
        if not description:
            return apology('must provide description', 403)
        
        if not day1 or not day2:
            return apology('date must incoude day', 403)
        
        if not month1 or not month2:
            return apology('date must incoude month', 403)
        
        if not year1 or not year2:
            return apology('date must incoude year', 403)
        
        db.execute('''
                   INSERT INTO tasks (user_id, title, description, dateCreation, dateStart, dateEnd, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ''', user_id, title, description, dateCreation, fDateStart, fDateEnd, status)
        
        flash('Task added successfully')

        return redirect('/')

    else:
        return render_template('addTask.html')
    

@app.route('/editTask', methods = ['GET', 'POST'])
@login_required
def editTask():

    def updateTask(task_id, user_id, title, description, dateStart, dateEnd):
        db.execute('''
                    UPDATE tasks
                    SET title = ?,
                        description = ?,
                        dateStart = ?,
                        dateEnd = ?
                    WHERE   id = ? AND user_id = ?
                    WHERE   title != ? AND
                            description != ? AND
                            dateStart != ? AND
                            dateEnd != ?
                    ''', title, description, dateStart, dateEnd, task_id, user_id, title, description, dateStart, dateEnd)
        
        flash('Task edited successfully')

        
    if request.method == 'POST':

        user_id = session['user_id']

        task_id = request.form.get('task')
    
        title = request.form.get('title')
        description = request.form.get('description')

        year1 = request.form.get('year1')
        month1 = request.form.get('month1')
        day1 = request.form.get('day1')
        
        if day1 != None and month1 != None and year1 != None:
            dateStart = dateForm(year1, month1, day1)
        
        else:
            dateStart = None
        
        year2 = request.form.get('year2')
        month2 = request.form.get('month2')
        day2 = request.form.get('day2')
        
        if day2 != None and month2 != None and year2 != None:
            dateEnd = dateForm(year2, month2, day2)

        else:
            dateEnd = None

        if description == 'Description':
            description = None
        
        if not title and not description and not dateStart and not dateEnd or description == 'Description':
            return apology('must provide at least one field to edit', 403)
        
        if title or description or dateStart or dateEnd:
            updateTask(task_id, user_id, title, description, dateStart, dateEnd)
            
        return redirect('/')

    else:
        user_id = session['user_id']

        user_tasks = db.execute('''SELECT *
                                FROM tasks
                                WHERE user_id = ?
                                ''', user_id)
        
        if user_tasks == []:
            return apology('you have no tasks to edit', 403)
                
        return render_template('editTask.html', tasks = user_tasks)


@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
        
        user_id = session['user_id']
        
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirmation = request.form.get('confirmation')
            day = request.form.get('day')
            month = request.form.get('month')
            year = request.form.get('year')

            if not name and not email and not password and not day and not month and not year:
                return apology('must provide at least one field to edit', 403)
            
            if password:
                if password != confirmation:
                    return apology('passwords do not match', 403)
                
                else:
                    password = generate_password_hash(password)

            if day != 'Day' and month != 'Month' and year != 'Year':
                fBirthDate = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            db.execute('''
                        UPDATE users
                        SET name = ?,
                            email = ?,
                            hashed_password = ?,
                            birthDate = ?
                        WHERE id = ? AND
                        name != ? OR
                        email != ? OR
                        hashed_password != ? OR
                        birthDate != ?
                        ''', name, email, password, fBirthDate, user_id, name, email, password, fBirthDate)
            
            flash('Profile edited successfully')

            return redirect('/')
        
        else:
            user_info = db.execute('''
                                      SELECT *
                                      FROM users
                                      WHERE id = ?
                                      ''', user_id)
            
            return render_template('profile.html', user_info = user_info)
        

@app.route('/completedTasks', methods = ['GET', 'POST'])
@login_required
def completedTasks():
    user_id = session['user_id']

    completed_tasks = db.execute('''
                                SELECT *
                                FROM tasks
                                WHERE user_id = ?
                                AND status = 'COMPLETED'
                                ''', user_id)
    
    if completed_tasks == []:
        return apology('you have no completed tasks', 403)
    
    return render_template('completedTasks.html', tasks = completed_tasks)


if __name__ == '__main__':
    app.run()