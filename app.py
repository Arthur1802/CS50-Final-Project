import os
import datetime

from cs50 import SQL
from flask import Flask, app, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db = SQL("sqlite:///list.db")

@app.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            return apology('Must provide username', 403)
        
        if not password:
            return apology('Must provide password', 403)
        
        # check = db.execute('''
        #                    SELECT *
        #                    FROM users
        #                    WHERE username = ? AND
        #                    password = ?
        #                    ''', username, password)
    
    else:
        return render_template('login.html')
        

@app.route('/register', methods = ['GET', 'POST'])
def register():
    return apology('TODO')