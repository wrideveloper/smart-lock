from flask import Flask
from flask_restful import Resource, reqparse,Api


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('uid')



class UserMasuk(Resource):

    def get(self):
        data = parser.parse_args()
        return data



api.add_resource(UserMasuk,'/smartlock/api/<uid>')
