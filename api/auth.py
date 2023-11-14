# auth.py
from flask_restx import Namespace, Resource, fields
from flask import request
from models.usuario import Usuario,Favorito
from flask_jwt_extended import (
    create_access_token
)

auth_ns = Namespace('auth', description='Operações de autenticação')

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='Nome de usuário'),
    'senha': fields.String(required=True, description='Senha'),
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('login')
    @auth_ns.expect(login_model)
    def post(self):
        '''Efetuar login'''
        login_data = request.json
        print(login_data)
        email = login_data.get('email')
        senha = login_data.get('senha')

        # Aqui, você deve verificar se o nome de usuário e a senha estão corretos.
        # Neste exemplo, assumimos que o login é bem-sucedido se o nome de usuário e a senha forem iguais.
        USUARIOS = Usuario.query.all()
        for usuario in USUARIOS:
            if usuario.email == email and email == senha:
                identity=str(usuario.id)+';'+str(usuario.id_perfil)
                access_token = create_access_token(identity=identity)
                return {"user_id": usuario.id, "perfil_id": usuario.id_perfil, "access_token": access_token , "message": "Login bem-sucedido"}, 200
            
        return {"message": "Login falhou, por favor verifique suas credenciais"}, 401
