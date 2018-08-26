from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flasktrainingcalendar import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    workouts = db.relationship('Workout', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            
        
    def followed_workouts(self):
        return Workout.query.join(
            followers, (followers.c.followed_id == Workout.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Workout.target_date)
    
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
        return 'User id: {0}, username: {1}, followed: {2}'.format(self.id, self.username, self.followed)


        
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_type = db.Column(db.String(100), nullable=False)
    workout_distance = db.Column(db.String(100), nullable=False)
    distance_unit = db.Column(db.String(100), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='workout', lazy=True)
    
    def __repr__(self):
        return 'Workout id: {0}, description: {1}{2}{3}, completed: {4}'.format(self.id, self.workout_distance, self.distance_unit, self.workout_type, self.completed)
        
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20))
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    
    def __repr__(self):
        return 'Photo id: {0}, image_file: {1}, workout_id: {2}'.format(self.id, self.image_file, self.workout_id)
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    
    def __repr__(self):
        return 'comment_id: {0}, user_id: {1}, workout_id: {2}, text: {3}'.format(self.id, self.user_id, self.workout_id, self.text)