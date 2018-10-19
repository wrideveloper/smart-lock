from flask import Flask
from flask import jsonify
from flask_restful import Resource
from flask_restful import Api
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
import datetime
import requests


app = Flask(__name__)


api = Api(app)


app.config[
    'SQLALCHEMY_DATABASE_URI'
] = 'sqlite:///wri/user.db'


db = SQLAlchemy(app)

""" Deklarasi Class """


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

        user_activity = LogActivity.query.filter_by(
            uid=uid, user_out=None
        ).first()

        if user_activity is None:

            add = LogActivity(uid=uid, user_in=tanggal)

            db.session.add(add)
            db.session.commit()

        elif user_activity and user_activity.user_out is None:

            user_activity.user_out = tanggal
            db.session.commit()


class Client:

    def user_masuk(self, uid):

        user_validation = User.query.filter_by(
            id=uid
        ).first()

        if user_validation:

            api_get = requests.get(
                'http://127.0.0.1:5000/smartlock/wri/api/v1/{}/'.format(
                    uid))

            if api_get.status_code == 200:

                print 'Selamat Datang Di Basecame WRI'

            else:
                abort()

    def user_keluar(self, uid):


        user_validation = User.query.filter_by(id=uid).first()

        if user_validation:

            gate_api = requests.get(
                'http://127.0.0.1:5000/smartlock/wri/api/v1/{}/'.format(
                    uid))

            if gate_api.status_code == 200:

                print "Selamat Jalan"

            else:

                abort()


""" API Route """


routes = [
    '/smartlock/wri/api/v1/<uid>/'
]

api.add_resource(PeriksaUid, *routes)


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
