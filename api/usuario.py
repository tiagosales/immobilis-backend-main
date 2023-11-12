from flask import request
from flask_restx import Namespace, Resource, fields
from api.admin import PERFIS,TELAS
from .utils import perfil_requerido
from datetime import datetime

# Cria um novo namespace do Flask-RESTX
usuario_ns = Namespace('usuarios', description='Operações de usuário')

# Define o modelo de dados do usuário usando o modelo do Flask-RESTX
user_model = usuario_ns.model('Usuario', {
    'id': fields.String(readOnly=True, description='Identificador único do usuário'),
    'nome': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='Endereço de e-mail do usuário'),
    'senha': fields.String(required=True, description='Senha do usuário'),
    'id_perfil': fields.Integer(required=True, description='Identificador do perfil do usuário'),
    'data_cadastro': fields.DateTime(readonly=True, description='Data de cadastro'),

})

favorito_model = usuario_ns.model('Favorito',{
     'id': fields.Integer(readOnly=True, description='Identificador único do favorito'),
     'id_usuario': fields.Integer(required=True, description='Identificador do usuário'),
     'id_imovel': fields.Integer(required=True, description='Identificador do imóvel'),
})

#Dados 
USUARIOS = [
     {
            "id": 1,
            "nome": "João",
            "email": "joao@teste.com",
            "senha": "senhasegura123",
            "id_perfil": 1,
            "data_cadastro": '2023-10-13'
        },
        {
            "id": 2,
            "nome": "Maria",
            "email": "maria@teste.com",
            "senha": "outrasenhasegura456",
            "id_perfil": 2,
            "data_cadastro": '2023-09-13'
        },
        {
            "id": 3,
            "nome": "Pedro",
            "email": "pedro@teste.com",
            "senha": "outrasenhasegura789",
            "id_perfil": 3,
            "data_cadastro": '2023-08-13'
        }
]

FAVORITOS = [
            {
                "id": 1,
                "id_usuario": 1,
                "id_imovel": 1001,
            },
            {
                "id": 2,
                "id_usuario": 1,
                "id_imovel": 1002,
            },
            {
                "id": 3,
                "id_usuario": 2,
                "id_imovel": 1010,
            },
            {
                "id": 4,
                "id_usuario": 2,
                "id_imovel": 1011,
            },
        ]

@usuario_ns.route('')
class ListaDeUsuarios(Resource):
    #@usuario_ns.doc('listar_usuarios')
    #@usuario_ns.doc(security='Bearer')
    #@perfil_requerido(['2','3'])
    def get(self):
        '''Listar todos os usuários'''
        return USUARIOS

    @usuario_ns.doc('criar_usuario')
    @usuario_ns.expect(user_model)
    def post(self):
        '''Criar um novo usuário'''
        novo_usuario = request.json
        novo_usuario['id'] = len(USUARIOS) + 1
        novo_usuario['data_cadastro'] = datetime.now().strftime('%Y-%m-%d')
        USUARIOS.append(novo_usuario)
        return novo_usuario, 201

@usuario_ns.route('/<int:id>')
@usuario_ns.response(404, 'Usuário não encontrado')
@usuario_ns.param('id', 'O identificador do usuário')
class Usuario(Resource):
    @usuario_ns.doc('obter_usuario')
    def get(self, id):
        '''Obter um usuário pelo identificador'''
        for usuario in USUARIOS:
            if usuario['id'] == id:
                return usuario
        usuario_ns.abort(404, f"Usuário {id} não encontrado")
    @usuario_ns.doc('update_user')
    @usuario_ns.expect(user_model)
    def put(self, id):
        '''Atualize um usuário pelo id'''
        user_to_update = None
        for user in USUARIOS:
            if user['id'] == id:
                user_to_update = user
                break
        if not user_to_update:
            usuario_ns.abort(404, f"Usuário {id} não encontrado")
        user_data = request.json
        user_to_update['nome'] = user_data['nome']
        user_to_update['email'] = user_data['email']
        user_to_update['id_perfil'] = user_data['id_perfil']
        return user_to_update
    
    @usuario_ns.doc('delete_user')
    def delete(self, id):
        '''Exclua um usuário pelo id'''
        user_to_delete = None
        for user in USUARIOS:
            if user['id'] == id:
                user_to_delete = user
                break
        if not user_to_delete:
            usuario_ns.abort(404, f"Usuário {id} não encontrado")
        USUARIOS.remove(user_to_delete)
        return '', 204

@usuario_ns.route('/<int:id>/favoritos')
@usuario_ns.response(404, 'Usuário não encontrado')
@usuario_ns.param('id', 'O identificador do usuário')

class FavoritosUsuario(Resource):
    @usuario_ns.doc('listar_favoritos_usuario')
    def get(self, id):
        '''Listar imóveis favoritos do usuário'''
        favoritos_tmp = []
        for favorito in FAVORITOS:
            if favorito['id_usuario'] == id:
                favoritos_tmp.append(favorito)
        return favoritos_tmp
    @usuario_ns.doc('inserir_favorito_usuario')
    @usuario_ns.expect(favorito_model)
    def post(self,id):
        '''Criar/Favoritar imóvel'''
        novo_favorito = request.json
        print(novo_favorito)
        for favorito in FAVORITOS:
            if id == favorito['id_usuario'] and novo_favorito['id_imovel'] == favorito['id_imovel']:
                return novo_favorito, 201
        novo_favorito['id'] = len(FAVORITOS) + 1
        novo_favorito['id_usuario'] = id
        FAVORITOS.append(novo_favorito)
        return novo_favorito, 201
    
@usuario_ns.route('/<int:id>/favoritos/<int:id_imovel>')
@usuario_ns.response(404, 'Usuário não encontrado')
@usuario_ns.param('id', 'O identificador do usuário')
@usuario_ns.param('id_imovel', 'O identificador do imovel')

class FavoritosUsuario(Resource):
    @usuario_ns.doc('apagar_favorito_usuario')
    def delete(self, id, id_imovel):
        '''Apagar favorito'''
        apagar_favorito = None
        for favorito in FAVORITOS:
            if favorito['id_usuario'] == id and favorito['id_imovel'] == id_imovel:
                apagar_favorito = favorito
                break
        if not apagar_favorito:
            usuario_ns.abort(404, f"Imovel favorito {id_imovel} não encontrado para o usuario {id}")
        FAVORITOS.remove(apagar_favorito)
        return '', 204
    
@usuario_ns.route('/<int:id>/telas-perfil')
@usuario_ns.response(404, 'Usuário não encontrado')
@usuario_ns.param('id', 'O identificador do usuário')
class TelasPerfil(Resource):
    @usuario_ns.doc('listar_perfil_telas')
    def get(self, id):
        '''Listar telas do usuário'''
        telasperfil_tmp = []
        if id == "0":
            telasperfil_tmp.append({'nome': 'Buscar Imóveis', "caminho": '/busca'})
        else:
            for usuario in USUARIOS:
                if usuario['id'] == id:
                    id_perfil = usuario['id_perfil']
            for perfil in PERFIS:
                if perfil['id'] == id_perfil:
                    for perfiltela in perfil['telas']:
                         for tela in TELAS:
                            if perfiltela == tela['id']:
                                telasperfil_tmp.append({'nome': tela['nome'], "caminho": tela['caminho']})

        return telasperfil_tmp
