from flask import Flask, render_template, request, url_for, redirect, session

import bcrypt

from models import app, db, User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(name=request.form['username']).first()
    if user is not None:
        if bcrypt.checkpw(request.form['pass'].encode('utf-8'), user.password_hash):
            session['username'] = request.form['pass']
            # print('You are logged in, ' + user.name)
            return redirect(url_for('index'))

        return 'Password is incorrect!'
    return 'User does not exists!'