# app/models.py

from flask_login import UserMixin
from app import db, login_manager, bcrypt


class User(UserMixin, db.Model):
    # Pastikan nama table plural
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(191), index=True, unique=True)
    username = db.Column(db.String(191), index=True, unique=True)
    first_name = db.Column(db.String(191), index=True)
    last_name = db.Column(db.String(191), index=True)
    password_hash = db.Column(db.String(191))
    tasks = db.relationship('Task', backref='user',lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        # membuat password read-only
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def verify_password(self, password):
        # check apakah password sama dengan yang di db
        return bcrypt.check_password_hash(self.password_hash, password)
    # representasi user
    def __repr__(self):
        return '<Username: {}>'.format(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(191))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<id: {}>'.format(self.id)

    def get_user(self):
        return User.query.filter_by(id=self.user_id).first()

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(191), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)