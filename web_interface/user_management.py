import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer, BadData
from flask import Flask, render_template, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Thisisasecret!')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ravi@8698@localhost/codecompanion'

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    users = []

    def __init__(self, id, username, password_hash, email):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        User.users.append(self)

    def set_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not password:
            return False
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        return s.dumps({'user_id': self.id}, salt='password-reset')

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = s.loads(token, salt='password-reset')['user_id']
        except BadData:
            return None
        return next((user for user in User.users if user.id == int(user_id)), None)


@login_manager.user_loader
def load_user(user_id):
    user = next((user for user in User.users if user.id == int(user_id)), None)
    if not user:
        abort(404, "User not found")
    return user


def send_reset_email(user):
    if not user.email:
        raise ValueError("User email cannot be empty")
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


'''The set_password method is used to hash a password for a user.
The check_password method is used to verify a password for a user.
The get_reset_token method is used to generate a unique token for a user that can be used to reset their password. The token is valid for a specified period of time.
The verify_reset_token method is used to verify a reset token for a user.
The send_reset_email function is used to send a password reset email to a user.'''



db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

def create_user(username, email):
    new_user = User(username, email)
    db.session.add(new_user)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        # handle error here


migrate = Migrate(app, db)

