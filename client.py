import requests
import json

class Client:
	server = 'http://10.42.0.215:5000'

        #metod buat buka pintu
	def open(self, uid):
		result = requests.get(self.server + '/activ')
		#return status pintu buka
		return result.json()['activ']

        #metod buat tutup pintu
	def lock(self):
		result = requests.get(self.server + '/activ')
		#return status pintu tutup
		return result.json()['activ']


if __name__ == '__main__':
	client = Client()
	#tampilin status di terminal
	print client.activ()
