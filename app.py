import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import apology, login_required

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


@app.route('/')
@login_required
def index():

    user_id = session['user_id']

    user_tasks = db.execute('''SELECT *
                            FROM tasks
                            WHERE user_id = ?
                            ''', user_id)
    
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
        return apology('TODO')

    else:
        return render_template('addTask.html')
    

@app.route('/editTask', methods = ['GET', 'POST'])
@login_required
def editTask():
    
        if request.method == 'POST':
            return apology('TODO')
    
        else:
            return render_template('editTask.html')
        

@app.route('/deleteTask', methods = ['GET', 'POST'])
@login_required
def deleteTask():
        
            if request.method == 'POST':
                return apology('TODO')
        
            else:
                return render_template('deleteTask.html')
            

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
        
        user_id = session['user_id']
        
        if request.method == 'POST':
            return apology('TODO')
        
        else:
            user_name = db.execute('''
                                      SELECT name
                                      FROM users
                                      WHERE id = ?
                                      ''', user_id)
            
            return render_template('profile.html', user_name = user_name[0]['name'])
        

@app.route('/get_profile_data')
@login_required
def get_profile_data():
    
    user_id = session['user_id']
    user_profile = db.execute('''
                              SELECT *
                              FROM users
                              WHERE id = ?
                              ''', user_id)
    
    return jsonify(user_profile[0])