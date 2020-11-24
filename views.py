from flask import Flask, render_template, request, url_for, redirect, session, g

import bcrypt

from models import app, db, User


@app.before_request
def before_request():
    g.user = session.get('username')


@app.route('/')
def index():
    if g.user:
        return 'Currently logged in as: ' + g.user
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(name=request.form['username']).first()
    if user is not None:
        if bcrypt.checkpw(request.form['pass'].encode('utf-8'), user.password_hash):
            session['username'] = request.form['username']
            # print('You are logged in, ' + user.name)
            return redirect(url_for('index'))

        return 'Password is incorrect!'
    return 'User does not exists!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_form = request.form['username']
        pwd_form = request.form['pass']
        username = User.query.filter_by(name=username_form).first()
        if not username:
            new_user = User(name=username_form, password_hash=bcrypt.hashpw(pwd_form.encode('utf-8'), bcrypt.gensalt()))
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username_form
            return redirect(url_for('index'))
        else:
            return 'User with such name already registered!'


    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))
