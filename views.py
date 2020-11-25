from flask import Flask, render_template, request, url_for, redirect, session, g

import bcrypt
from datetime import datetime

from models import app, db, User, Exercises, Workout, Exercise, Set


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
            return redirect(url_for('add_workout'))

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
            return redirect(url_for('add_workout'))
        else:
            return 'User with such name already registered!'


    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/add_workout', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        user = User.query.filter_by(name=session['username']).first()
        workout = Workout(date=datetime.utcnow(), user_id=user.id)

        exercise_count = int(request.form['exercise_count'])
        for exercise_num in range(1, exercise_count+1):
            exercise = Exercise(order=1, exercise_id=request.form['exercise' + str(exercise_num)], workout=workout)
            weights = request.form.getlist('weight' + str(exercise_num))
            reps = request.form.getlist('reps' + str(exercise_num))

            set_order = 1
            for weight, rep in zip(weights, reps):
                work_set = Set(order=set_order, exercise=exercise, weight=weight, reps=reps)
                set_order += 1

        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('index'))

    exercises = Exercises.query.all()
    return render_template('add_workout.html', exercises=exercises)
