from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3
import os

app = Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['FLASKS3_BUCKET_NAME'] = os.environ.get('AWS_STORAGE_BUCKET_NAME')
s3 = FlaskS3(app)

workouts = [
    {
        'type': '5k Run',
        'description': '5k Run',
        'target_date': 'July 06, 2018'
    },
    {
        'type': '3k Workout Run',
        'description': '3k Tempo Run',
        'target_date': 'July 08, 2018'
    },
    {
        'type': '10K Long Run',
        'description': '10K Long slow run',
        'target_date': 'July 10, 2018'
    }
]


@app.route('/')
def hello():
    return render_template("home.html")
    
@app.route('/workouts')
def get_workouts():
    return render_template("workouts.html", workouts=workouts, title="workouts")
    
@app.route('/register')
def register():
    form = RegistrationForm
    return render_template("register.html", title="register", form=form)
    
@app.route('/login')
def login():
    form = LoginForm
    return render_template("login.html", title="login", form=form)
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)