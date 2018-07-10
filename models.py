from datetime import datetime
import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    workouts = db.relationship('Workout', backref='author', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username 
        
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_type = db.Column(db.String(100), nullable=False)
    target_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return '<Workout %r>' % self.workout_type