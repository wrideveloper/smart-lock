from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api , reqparse, abort


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)

#database
app.config['SECERET_KEY'] = 'kjaiufdknd5433342!@#$%^&*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dt_admin:yafi2105@localhost/project'



#route
@app.route('/')
def home():
    return 'Hello World'



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
