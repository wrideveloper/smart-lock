from flask import Flask
from flask_restful import Resource, Api
import datetime, requests


app = Flask(__name__)
api = Api(app)


#route sementara
@app.route('/')
def index():
    return 'hello'


"""
Dibawah ini akan menjadi API configurasi,route & Resource

"""
class PeriksaUid(Resource):

    def get(self,uid):

        tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = []

        uid_data = {

            'date' : str(tanggal),
            'udi' : uid
        }
        data.append(uid_data)

        return {'message' : 'Data berhasil di tambah','data' : data}




routes = [

    '/smartlock/wri/api/v1/<uid>'
]
api.add_resource(PeriksaUid,*routes)

'''
fungsi untuk client
'''

class Client:

    def masuk(self,uid):

        req = requests.get('http://127.0.0.1:5000/smartlock/wri/api/v1/{}'.format(uid))





if __name__ == '__main__':

    app.run(debug = True,host = '0.0.0.0')
