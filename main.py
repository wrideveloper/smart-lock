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
from MFRC522.Read import detected

sys.path.append('Stepper')
from Stepper import open

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
        uid = uid, user_in = None
    ).first()

    if otomat_validation is None:
        user_masuk_keluar(uid)

def user_masuk_keluar(uid):

    user_validation = User.query.filter_by(
        id=uid
    ).first()

    if user_validation:

        api_get = requests.get('http://127.0.0.1:5000/smartlock/wri/api/v1/{}/'.format(uid))

        if api_get.status_code == 200:

            open()
            print 'Selamat Datang Di WRI Politeknik Negeri Malang'

        else:
            abort()

"""Fungsi Read RFID"""
def main():
    read = True
    while read :

    # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"

    # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
        if status == MIFAREReader.MI_OK:


        # print uid
            print "card read uid: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])

        # this is the default key for authentication
            key = [0xff,0xff,0xff,0xff,0xff,0xff]

        # select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

        #liat isi tag di sector8  (array isi 16)
            MIFAREReader.MFRC522_Read(8)
        #turn on led
            GPIO.setup(8, GPIO.OUT)
            GPIO.output(8, GPIO.HIGH)
        #stop looping
            time.sleep(3)
            continue_reading = False
            GPIO.output(8, GPIO.LOW)
            read = False
            return True
            GPIO.cleanup()


""" API Route """


routes = [
    '/smartlock/wri/api/v1/<uid>/'
]

api.add_resource(PeriksaUid, *routes)


if __name__ == '__main__':
    main()
    app.run(debug=True)
