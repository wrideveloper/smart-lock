from admin import admin as admin_blueprint
from Stepper import open
from flask import Flask
from flask import jsonify
from flask_restful import Resource
from flask_restful import Api
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_bootstrap import Bootstrap
import requests
import RPi.GPIO as GPIO
from MFRC522 import MFRC522
import time
import sys
#from MFRC522.Read import detected

sys.path.append('Stepper')

app = Flask(__name__)
Bootstrap(app)


login_manager = LoginManager()
api = Api(app)

app.config['SECRET_KEY'] = 'ProjectWRI1231'
app.config[
    'SQLALCHEMY_DATABASE_URI'
] = 'sqlite:///wri/user.db'


db = SQLAlchemy(app)

# Blueprint
app.register_blueprint(admin_blueprint)


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.String(18), primary_key=True)
    username = db.Column(db.String(18))

    def __repr__(self):

        return '<User : {}>'.format(self.id)


class LogActivity(db.Model):

    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(18))
    user_in = db.Column(db.DateTime())
    user_out = db.Column(db.DateTime())
    status = db.Column(db.Boolean(), default=False)

    def __repr__(self):

        return '<LogActivity: {}>'.format(self.uid)


class UserWeb(UserMixin, db.Model):

    __tablename__ = 'pengguna'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    password_has = db.Column(db.String(255))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<UserWeb: {}>'.format(self.username)

# Set up user_loader


@login_manager.user_loader
def load_user(user_id):


return UserWeb.query.get(int(user_id))


class PeriksaUid(Resource):

    def get(self, uid):
        tanggal = datetime.datetime.now()
        user_validation = User.query.filter_by(
            id=uid
        ).first()

        if user_validation:
            user_log = LogActivity.query.filter_by(
                uid=uid, user_out=None
            ).first()

            if user_log is None:
                add_log = LogActivity(uid=uid, user_in=tanggal)
                db.session.add(add_log)
                db.session.commit()
            elif user_log and user_log.user_out is None:
                user_log.user_out = tanggal
                db.session.commit()

        else:

            print 'tidak ada'


routes = [
    '/smartlock/wri/api/v1/<uid>/'
]

api.add_resource(PeriksaUid, *routes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
