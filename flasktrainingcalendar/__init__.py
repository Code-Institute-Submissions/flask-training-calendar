from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
app.config['FLASKS3_BUCKET_NAME'] = os.environ.get('AWS_STORAGE_BUCKET_NAME')
s3 = FlaskS3(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from flasktrainingcalendar import routes