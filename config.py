from flask import Flask,Blueprint
from flask_restx import Api
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt 



load_dotenv()

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint,authorizations=authorizations, security='Bearer')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)
CORS(app)
app.register_blueprint(blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app) 

# Configuração do OAuth para o Google
app.config['OAUTH2_PROVIDERS'] = {
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
    },
}
