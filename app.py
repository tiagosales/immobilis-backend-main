from config import app, db, migrate,api

from api.usuario import usuario_ns
from api.imovel import imovel_ns
from api.mensagem import mensagem_ns
from api.admin import admin_ns
from api.auth import auth_ns 
from api.localizacao import localizacao_ns
from api.acesso import acesso_ns

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