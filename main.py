
import requests
from server import app

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

		result = requests.get('10.42.0.215:5000/smartlock/api/{}'.format(uuid))
		message = {'status' : 'berhasil'}
		return message

if __name__ == '__main__':
    app.run(debug = True,host = '0.0.0.0')
