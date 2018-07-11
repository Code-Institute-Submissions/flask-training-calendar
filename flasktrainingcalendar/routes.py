import os
import random
import string
import boto3
from flask import Flask, render_template, url_for, flash, redirect, request
from flasktrainingcalendar import app, db, bcrypt
from flasktrainingcalendar.models import User, Workout
from flasktrainingcalendar.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewWorkoutForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    return render_template("home.html")
    
@app.route('/workouts')
def get_workouts():
    workouts = Workout.query.all()
    return render_template("workouts.html", workouts=workouts, title="workouts")
    
@app.route('/register', methods=['POST', "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hash_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been successfully created, please login", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="register", form=form)
    
@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.username_or_email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        if user is None:
            user = User.query.filter_by(username = form.username_or_email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('You have been logged in!', 'success')
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check your login details', 'danger')
        else:
            flash('Login Unsuccessful. Please check your login details', 'danger')
    return render_template("login.html", title="login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    


def save_picture(form_picture):          
    random_hex = ''.join([random.choice(string.digits) for n in range(8)])    
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = random_hex + f_ext
    s3 = boto3.resource('s3')
    s3.Bucket('mpark-flask-training-calendar').put_object(Key="static/profile_pics/" + picture_fn, Body=form_picture)
    return picture_fn   
    

@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been successfully updated", "success")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='account', form=form)
    
@app.route("/workout/new", methods=["POST", "GET"])
@login_required
def new_workout():
    form = NewWorkoutForm()
    if form.validate_on_submit():
        workout = Workout(workout_type = form.workout_type.data, target_date = form.target_date.data, description = form.description.data, user_id=current_user.id)
        db.session.add(workout)
        db.session.commit()
        flash('Your Workout has been added', 'success')
        return redirect(url_for('get_workouts'))
    return render_template('new_workout.html', title='New Workout', form=form)