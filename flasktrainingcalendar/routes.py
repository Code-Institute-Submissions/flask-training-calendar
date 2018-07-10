from flask import Flask, render_template, url_for, flash, redirect
from flasktrainingcalendar import app, db, bcrypt
from flasktrainingcalendar.models import User, Workout
from flasktrainingcalendar.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user

workouts = [
    {
        'workout_type': '5k Run',
        'description': '5k Run',
        'target_date': 'July 06, 2018'
    },
    {
        'workout_type': '3k Workout Run',
        'description': '3k Tempo Run',
        'target_date': 'July 08, 2018'
    },
    {
        'workout_type': '10K Long Run',
        'description': '10K Long slow run',
        'target_date': 'July 10, 2018'
    }
]



@app.route('/')
def home():
    return render_template("home.html")
    
@app.route('/workouts')
def get_workouts():
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
            return redirect(url_for('home'))
        if user is None:
            user = User.query.filter_by(username = form.username_or_email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check your login details', 'danger')
        else:
            flash('Login Unsuccessful. Please check your login details', 'danger')
    return render_template("login.html", title="login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))