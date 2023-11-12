from flask import Flask,Blueprint
from flask_restx import Api
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)
from api.usuario import usuario_ns
from api.imovel import imovel_ns
from api.mensagem import mensagem_ns
from api.admin import admin_ns
from api.auth import auth_ns 
from api.localizacao import localizacao_ns
from api.acesso import acesso_ns

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
app.config['SECRET_KEY'] = 'devkey'
jwt = JWTManager(app)
CORS(app)
app.register_blueprint(blueprint)

# Register the user API with the application
api.add_namespace(usuario_ns)
api.add_namespace(imovel_ns)
api.add_namespace(mensagem_ns)
api.add_namespace(admin_ns)
api.add_namespace(auth_ns)
api.add_namespace(localizacao_ns)
api.add_namespace(acesso_ns)


if __name__ == '__main__':
    app.run(debug=True)