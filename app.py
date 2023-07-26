import os
from datetime import datetime
import random
import sqlite3

from cs50 import SQL
from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import *

app = Flask(__name__)

db = SQL('sqlite:///tasktracker.db')

# conn = sqlite3.connect('tasktracker.db')
# db = conn.cursor()

@app.route('/')
@login_required
def index():

    user_id = session['user_id']

    user_tasks = db.execute('''
                            SELECT *
                            FROM tasks
                            WHERE user_id = ?
                            ''', user_id)
    
    return render_template('index.html', user_tasks = user_tasks)


@app.route('/register', methods = ['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        birthDate = request.form.get('birthDate')
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
                                 INSERT INTO users (name, email, hashed_password, dateBirth DATE)
                                 ''', name, email, generate_password_hash(password), fBirthDate)
        
        session['user_id'] = new_session
        
    else:
        return render_template('register.html')
    

app.route('/login', methods = ['GET', 'POST'])
def login():
    '''Log user in'''

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get('username'):
            return apology('must provide username', 403)

        # Ensure password was submitted
        elif not request.form.get('password'):
            return apology('must provide password', 403)

        # Query database for username
        rows = db.execute('SELECT * FROM users WHERE username = ?', request.form.get('username'))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], request.form.get('password')):
            return apology('invalid username and/or password', 403)

        # Remember which user has logged in
        session['user_id'] = rows[0]['id']

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')
    

@app.route('/logout')
def logout():
    '''Log user out'''

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect('/')