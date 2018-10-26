from flask import Flask
from flask import jsonify
from flask_restful import Resource
from flask_restful import Api
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
import datetime
import requests
import RPi.GPIO as GPIO
# from MFRC522 import MFRC522
import MFRC522

import time
import sys
# from MFRC522.Read import detected


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


"""Fungsi Untuk Validasi"""


def cek_status(uid):
    otomat_validation = LogActivity.query.filter_by(
        uid=uid, user_in=None
    ).first()

    if otomat_validation is None:
        user_masuk_keluar(uid)


def user_masuk_keluar(uid):

    user_validation = User.query.filter_by(
        id=uid
    ).first()

    if user_validation:

        api_get = requests.get(
            'http://127.0.0.1:5000/smartlock/wri/api/v1/{}/'.format(uid))

        if api_get.status_code == 200:

            print 'Selamat Datang Di WRI Politeknik Negeri Malang'

        else:
            abort()


"""Fungsi Read RFID"""


def reading(self, continue_reading):
    while continue_reading:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print "Card detected"
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            autentikasi(status, uid)


def autentikasi(self, status, uid):
    print "card read uid: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
    uuid = "%s%s%s%s" % (uid[0], uid[1], uid[2], uid[3])

    key = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]

    MIFAREReader.MFRC522_SelectTag(uid)
    status = MIFAREReader.MFRC522_Auth(
        MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

    # Check if authenticated
    if status == MIFAREReader.MI_OK:
        MIFAREReader.MFRC522_Read(8)
        client.cek_status(str(uuid))
        MIFAREReader.MFRC522_StopCrypto1()
        end_read()
    else:
        print "Authentication error"


def end_read(signal, frame):
    # global continue_reading
    print "Ctrl+C captured, ending read."
    #continue_reading = False
    GPIO.cleanup()


""" API Route """


routes = [
    '/smartlock/wri/api/v1/<uid>/'
]

api.add_resource(PeriksaUid, *routes)


if __name__ == '__main__':
    # main()
    app.run(debug=True)
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()
    print "Welcome to the Workshop Riset Infromatika"
    global continue_reading = True
    reading(continue_reading)
