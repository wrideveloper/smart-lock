from flask import Flask
from flask import jsonify
from flask_restful import Resource
from flask_restful import Api
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
import datetime
import requests
import RPi.GPIO as GPIO

from  MFRC522 import  MFRC522
import time
import sys
#from MFRC522.Read import detected

sys.path.append('Stepper')
from Stepper import open

app = Flask(__name__)


api = Api(app)


app.config[
    'SQLALCHEMY_DATABASE_URI'
] = 'sqlite:///wri/user.db'


db = SQLAlchemy(app)




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


class PeriksaUid(Resource):

    def get(self, uid):
        tanggal = datetime.datetime.now()
        user_validation = User.query.filter_by(
            id = uid
        ).first()

        if user_validation:
            user_log = LogActivity.query.filter_by(
            uid = uid, user_out = None
            ).first()

            if user_log is None:
                add_log = LogActivity(uid = uid,user_in = tanggal)
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
    app.run(debug=True)
