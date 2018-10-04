from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api , reqparse, abort


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)

#database
app.config['SECERET_KEY'] = 'kjaiufdknd5433342!@#$%^&*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dt_admin:yafi2105@localhost/project'




#database model
class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10))
    activitie = db.relationship("Activities",uselist = False,back_populates = "usr")

    @property
    def serializable(self):
        return {'id' : self.id, 'username' : self.username}


class Activities(db.Model):

    __tablename__ = 'activities'

    activities_id = db.Column(db.Integer, primary_key = True)
    activ = db.Column(db.Boolean, default = False)
    time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usr = db.relationship("User", back_populates = "activitie")

    @property
    def serializable(self):
        return {'activities_id' : self.activities_id, 'activ' : self.activ,
        'time' : self.time,'user_id' : self.user_id}

#route
@app.route('/')
def home():
    return 'Hello World'


class Coba(Resource):

    def get(self):
        return {'Status' : 'JANCUK'}


api.add_resource(Coba,'/coba/api/hello/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True, host = '0.0.0.0')
