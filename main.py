#import RPi.GPIO as GPIO
#from .MFRC522 import Read
#from client import Client
#from Solenoid import Solenoid (kalo udah ada)
import requests
#from server import app

"""
reading = Read() #instansiasi class Read.py
client = Client() #instansiasi class lient.py

while True:
	if reading.detected(): #jika kartu terdeteksi
				uid = reading.getUid()
                client.open(uid) # return activity ke webservice
		#solenoid.open() kalo udah ada

	else:
		client.lock()
		#solenoid.open() kalo udah ada

class getUid(self,uid)
"""

class Client:

	def masuk(self,uuid):

		result = requests.get('http://172.16.123.5:5000/smartlock/api/{}'.format(uuid))

		return result.json()['status']
