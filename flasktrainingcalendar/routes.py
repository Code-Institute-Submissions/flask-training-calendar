import os
import random
import string
import boto3
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flasktrainingcalendar import app, db, bcrypt, mail
from flasktrainingcalendar.models import User, Workout, Photo
from flasktrainingcalendar.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewWorkoutForm, CompletedWorkoutForm, WorkoutPhotoForm, RequestResetForm, ResetPasswordForm, UserSearchForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date
from flask_mail import Message

@app.route('/')
def home():
    if current_user.is_authenticated:
        workouts = Workout.query.filter_by(user_id = current_user.id, target_date=date.today(), completed=False).all()
        return render_template("home.html", workouts=workouts)
    return render_template("home.html")

@app.route('/workouts')
def get_workouts():
    page = request.args.get('page', 1, type=int)
    workouts = Workout.query.filter_by(user_id = current_user.id, completed=False).order_by(Workout.target_date).paginate(page=page, per_page=9)
    return render_template("workouts.html", workouts=workouts, title="workouts")
    
@app.route('/workouts/completed')
def get_completed_workouts():
    page = request.args.get('page', 1, type=int)
    workouts = Workout.query.filter_by(user_id = current_user.id, completed=True).order_by(Workout.target_date.desc()).paginate(page=page, per_page=9)
    return render_template("completed_workouts.html", workouts=workouts, title="completed workouts")
    
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
    


def save_profile_picture(form_picture):          
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
            picture_file = save_profile_picture(form.picture.data)
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
        workout = Workout(workout_type = form.workout_type.data, workout_distance = form.workout_distance.data, distance_unit = form.distance_unit.data, target_date = form.target_date.data, description = form.description.data, user_id=current_user.id)
        db.session.add(workout)
        db.session.commit()
        flash('Your Workout has been added', 'success')
        return redirect(url_for('get_workouts'))
    return render_template('new_workout.html', title='New Workout', form=form, legend='Add A Workout')
    


def save_workout_picture(form_picture):          
    random_hex = ''.join([random.choice(string.digits) for n in range(8)])    
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = random_hex + f_ext
    s3 = boto3.resource('s3')
    s3.Bucket('mpark-flask-training-calendar').put_object(Key="static/workout_pics/" + picture_fn, Body=form_picture)
    return picture_fn 


@app.route("/workout/<int:workout_id>", methods=["POST", "GET"])
def workout(workout_id):
    workout=Workout.query.get_or_404(workout_id)
    photos = Photo.query.filter_by(workout_id=workout.id).all()
    if workout.user_id != current_user.id and not current_user.is_following(workout.author):
        return redirect(url_for('get_workouts'))
    completed_form = CompletedWorkoutForm()
    if completed_form.submit.data and completed_form.validate_on_submit():
        workout.completed = True
        db.session.commit()
        flash('You have marked this workout as completed', 'success')
        return redirect(url_for('workout', workout_id=workout.id))
    photo_form = WorkoutPhotoForm()
    if photo_form.upload.data and photo_form.validate_on_submit():
        picture_file = save_workout_picture(photo_form.picture.data)
        photo = Photo(image_file=picture_file, workout_id=workout.id)
        db.session.add(photo)
        db.session.commit()
        return redirect(url_for("workout", workout_id=workout.id))
    return render_template("workout.html", title=workout.workout_type, workout=workout, photos=photos, completed_form=completed_form, photo_form=photo_form)
    
@app.route("/workout/<int:workout_id>/update", methods=["GET", "POST"])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        abort(403)
    form = NewWorkoutForm()
    if form.validate_on_submit():
        workout.workout_type = form.workout_type.data
        workout.workout_distance = form.workout_distance.data
        workout.distance_unit = form.distance_unit.data
        workout.description = form.description.data
        workout.target_date = form.target_date.data
        db.session.commit()
        flash("Your workout has been updated!", "success")
        return redirect(url_for('workout', workout_id=workout.id))
    elif request.method == "GET":
        form.workout_type.data = workout.workout_type
        form.workout_distance.data = workout.workout_distance
        form.distance_unit.data = workout.distance_unit
        form.description.data = workout.description
        form.target_date.data = workout.target_date
    return render_template('new_workout.html', title='Update Post', form=form, legend='Update Workout')
    
@app.route("/workout/<int:workout_id>/delete", methods=["POST"])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    photos = Photo.query.filter_by(workout_id=workout.id).all()
    if workout.user_id != current_user.id:
        abort(403)
    db.session.delete(workout)
    db.session.commit()
    for photo in photos:
        db.session.delete(photo)
        db.session.commit()
    flash("Your post has been deleted", "success")
    return redirect(url_for('get_workouts'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = "To reset your password visit the following link: " + (url_for('reset_token', token=token, _external=True))
    mail.send(msg)
    
@app.route("/reset_password", methods=["POST", "GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.username_or_email.data).first()
        if user is None:
            user = User.query.filter_by(username = form.username_or_email.data).first()
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password', 'info')
            return redirect(url_for('login'))
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)
    
@app.route("/reset_password/<token>", methods=["POST", "GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_password
        db.session.commit()
        flash("Your password has been updated, please login", "success")
        return redirect(url_for("login"))
    return render_template('reset_token.html', title='Reset Password', form=form)
    
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("No such user exists", "warning")
        return redirect(url_for("following"))
    if user == current_user:
        flash("You can not follow yourself", "warning")
        return redirect(url_for("following"))
    current_user.follow(user)
    db.session.commit()
    flash("You are now following {0}".format(username), "success")
    return redirect(url_for("view_user", username=user.username))
    
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("No such user exists", "warning")
        return redirect(url_for("following"))
    if user == current_user:
        flash("You can not unfollow yourself", "warning")
        return redirect(url_for("following"))
    current_user.unfollow(user)
    db.session.commit()
    flash("You are no longer following {0}".format(username), "success")
    return redirect(url_for("following"))
    
@app.route('/following', methods=["POST", "GET"])
def following():
    all_users = User.query.all()
    users = [user for user in all_users if current_user.is_following(user)]
    form = UserSearchForm()
    if form.validate_on_submit():
        username = form.search.data
        user = User.query.filter_by(username = username).first()
        if user is None:
            flash("That user does not exist", "warning")
            return redirect(url_for("following"))
        return redirect(url_for("view_user", username=user.username))
    return render_template("following.html", users=users, form=form)
    
@app.route('/user/<username>')
@login_required
def view_user(username):
    user = User.query.filter_by(username=username).first()
    if user == current_user:
        return redirect(url_for("account"))
    page = request.args.get('page', 1, type=int)
    workouts = Workout.query.filter_by(user_id = user.id, completed=False).order_by(Workout.target_date).paginate(page=page, per_page=9) 
    return render_template('user.html', user=user, workouts = workouts)
    
@app.route('/user/<username>/completed')
@login_required
def view_user_completed(username):
    user = User.query.filter_by(username=username).first()
    if user == current_user:
        return redirect(url_for("account"))
    if not current_user.is_following(user):
        flash("You are not following that user", "warning")
        return redirect(url_for("following"))
    page = request.args.get('page', 1, type=int)
    workouts = Workout.query.filter_by(user_id = user.id, completed=True).order_by(Workout.target_date.desc()).paginate(page=page, per_page=9) 
    return render_template('user_completed.html', user=user, workouts = workouts)