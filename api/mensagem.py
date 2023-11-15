from flask import request
from flask_restx import Namespace, Resource, fields
from models.mensagem import Mensagem
from config import db
from datetime import datetime
from models.imovel import Imovel



# Crie um novo namespace para mensagens
mensagem_ns = Namespace('mensagens', description='Operações relacionadas a mensagens')
mensagem_model = mensagem_ns.model('Mensagem', {
    'id': fields.Integer(readonly=True, description='ID da mensagem'),
    'texto': fields.String(required=True, description='Texto da mensagem'),
    'id_usuario_remetente': fields.Integer(required=True, description='ID do usuário remetente'),
    'id_usuario_destinatario': fields.Integer(required=False, description='ID do usuário destinatário'),
    'nome': fields.Integer(required=True, description='Nome do usuário remetente'),
    'data': fields.DateTime(required=True, description='Data de envio da mensagem'),
    'email': fields.String(required=True, description='Email do remetente'),
    'id_imovel': fields.Integer(required=True, description='ID do imóvel relacionado à mensagem'),
})
#Dados do mock
'''INSERT INTO mensagem (id, id_usuario_remetente, id_usuario_destinatario, id_imovel, nome, texto, email, data, lida)
VALUES (1, 0, 2, 1001, 'Daniel Federer', 'Gostaria de visitar o imóvel! Por favor entre em contato no meu email!', 'teste@teste.com', '2022-10-02', false);'''

# Função para serializar objetos datetime
def serialize_datetime(dt):
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


# Função para converter objetos Mensagem em dicionários
def mensagem_to_dict(mensagem):
    return {
        'id': mensagem.id,
        'texto': mensagem.texto,
        'nome': mensagem.nome,
        'data': serialize_datetime(mensagem.data),
        'id_usuario_remetente': mensagem.id_usuario_remetente,
        'id_usuario_destinatario': mensagem.id_usuario_destinatario,
        'email': mensagem.email,
        'id_imovel': mensagem.id_imovel
    }

@mensagem_ns.route('/<int:id>')
@mensagem_ns.response(404, 'Usuário não encontrado')
@mensagem_ns.param('id', 'O identificador do usuário')
class MensagensUsuario(Resource):
    @mensagem_ns.doc('listar_mensagens_usuario')
    def get(self, id):
        '''Listar mensagens do usuário'''
        mensagens = Mensagem.query.filter_by(id_usuario_destinatario=id).order_by(Mensagem.data.desc()).all()
        return [mensagem_to_dict(mensagem) for mensagem in mensagens]

@mensagem_ns.route('/')
@mensagem_ns.response(404, 'Usuário não encontrado')
@mensagem_ns.param('id', 'O identificador do usuário')
class Mensagens(Resource):
    @mensagem_ns.doc('criar_mensagem')
    @mensagem_ns.expect(mensagem_model)
    def post(self):
        '''Criar uma nova mensagem'''
        nova_mensagem = mensagem_ns.payload
        id_imovel = nova_mensagem['id_imovel']
        id_usuario_destinatario = db.session.query(Imovel.id_usuario).filter_by(id=id_imovel).scalar()
        nova_mensagem['id_usuario_destinatario'] = id_usuario_destinatario
        if id_usuario_destinatario is None:
            mensagem_ns.abort(404, f"Imóvel {id_imovel} não encontrado")
        mensagem = Mensagem(
            texto=nova_mensagem['texto'],
            id_usuario_remetente=nova_mensagem['id_usuario_remetente'],
            id_usuario_destinatario=nova_mensagem['id_usuario_destinatario'],
            nome=nova_mensagem['nome'],
            data=serialize_datetime(datetime.now()),
            email=nova_mensagem['email'],
            id_imovel=nova_mensagem['id_imovel']
        )
        db.session.add(mensagem)
        db.session.commit()
        return {'id': mensagem.id, 'texto': mensagem.texto, 'nome': mensagem.nome, 'data': serialize_datetime(mensagem.data)}, 201