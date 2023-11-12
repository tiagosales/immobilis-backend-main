from flask import request
from flask_restx import Namespace, Resource, fields

# Crie um novo namespace para acessos
acesso_ns = Namespace('acessos', description='Operações relacionadas a acessos')

# Defina o modelo da acesso
acesso_model = acesso_ns.model('Mensagem', {
    'id': fields.Integer(readonly=True, description='ID da acesso'),
    'id_usuario': fields.Integer(required=True, description='ID do usuário'),
    'data_acesso': fields.DateTime(required=True, description='Data do acesso'),
    'caminho': fields.String(required=True, description='Caminho acessado'),
})

ACESSOS = [
            {
                "id": 1,
                "id_usuario": 1,
                "data_acesso": "2023-03-30T12:00:00",
                "caminho": "/api/v1/imoveis/1001",
            },
            {
                "id": 2,
                "id_usuario": 2,
                "data_acesso": "2023-03-31T09:00:00",
                "caminho": "/api/v1/usuarios/2/favoritos",
            },
        ]

@acesso_ns.route('/')
class Acessos(Resource):
    @acesso_ns.doc('listar_acessos')
    def get(self):
        '''Listar acessos'''
        return ACESSOS, 200
    
    @acesso_ns.doc('criar_registro_acesso')
    @acesso_ns.expect(acesso_model)
    def post(self):
        '''Criar um novo registro de acesso'''
        novo_acesso = acesso_ns.payload
        novo_acesso['id'] = len(ACESSOS) + 1
        ACESSOS.append(novo_acesso)
        return novo_acesso, 201
    
    