from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3
import os

app = Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['FLASKS3_BUCKET_NAME'] = os.environ.get('AWS_STORAGE_BUCKET_NAME')
s3 = FlaskS3(app)

from flasktrainingcalendar import routes