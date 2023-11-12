from flask import request
from .imovel import IMOVEIS
from flask_restx import Namespace, Resource, fields

# Crie um novo namespace para mensagens
mensagem_ns = Namespace('mensagens', description='Operações relacionadas a mensagens')

# Defina o modelo da mensagem
mensagem_model = mensagem_ns.model('Mensagem', {
    'id': fields.Integer(readonly=True, description='ID da mensagem'),
    'texto': fields.String(required=True, description='Texto da mensagem'),
    'id_usuario_remetente': fields.Integer(required=True, description='ID do usuário remetente'),
    'id_usuario_destinatario': fields.Integer(required=False, description='ID do usuário destinatário'),
    'nome': fields.Integer(required=True, description='Nome do usuário remetente'),
    'data': fields.DateTime(required=True, description='Data de envio da mensagem'),
    'email': fields.String(required=True, description='Email do remetente'),
    'lida': fields.Boolean(description='Indica se a mensagem foi lida'),
    'id_imovel': fields.Integer(required=True, description='ID do imóvel relacionado à mensagem'),
})

# Lista de mensagens 
MENSAGENS = [
            {
                "id": 1,
                "id_usuario_remetente": 0,
                "id_usuario_destinatario": 2,
                "id_imovel": 1001,
                "nome": "Daniel Federer",
                "texto": "Gostaria de visitar o imovel! Por favor entre em contato no meu email!",
                "email": "teste@teste.com",
                "data": "2022-10-02",
                "lida": False,
            },
            ]
@mensagem_ns.route('/<int:id>')
@mensagem_ns.response(404, 'Usuário não encontrado')
@mensagem_ns.param('id', 'O identificador do usuário')
class MensagensUsuario(Resource):
    @mensagem_ns.doc('listar_mensagens_usuario')
    def get(self, id):
        '''Listar mensagens do usuário'''
        mensagens_tmp = []
        for mensagem in MENSAGENS:
            if mensagem['id_usuario_destinatario'] == id:
                mensagens_tmp.append(mensagem)
        return mensagens_tmp
    
@mensagem_ns.route('/')
@mensagem_ns.response(404, 'Usuário não encontrado')
@mensagem_ns.param('id', 'O identificador do usuário')
class Mensagens(Resource):
    @mensagem_ns.doc('criar_mensagem')
    @mensagem_ns.expect(mensagem_model)
    def post(self):
        '''Criar uma nova mensagem'''
        nova_mensagem = mensagem_ns.payload
        nova_mensagem['id'] = len(MENSAGENS) + 1
        for imovel in IMOVEIS:
            if nova_mensagem['id_imovel'] == imovel['id']:
                nova_mensagem['id_usuario_destinatario'] = imovel['id_usuario']
        MENSAGENS.append(nova_mensagem)
        return nova_mensagem, 201
    
    