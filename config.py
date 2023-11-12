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
