from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flasktrainingcalendar import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    workouts = db.relationship('Workout', backref='author', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s =Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod    
    def verify_reset_token(token):
        s =Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return '<User %r>' % self.username 

        
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_type = db.Column(db.String(100), nullable=False)
    workout_distance = db.Column(db.String(100), nullable=False)
    distance_unit = db.Column(db.String(100), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return '<Workout %r>' % self.workout_type
        
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20))
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    
    def __repr__(self):
        return '<Photo id: {0}, image_file: {1}, workout_id: {2}>'.format(self.id, self.image_file, self.workout_id)