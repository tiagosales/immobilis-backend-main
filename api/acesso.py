from flask import request
from flask_restx import Namespace, Resource, fields
from models.acesso import Acesso
from config import db
from datetime import datetime
from .utils import perfil_requerido


# Função para serializar objetos datetime
def serialize_datetime(dt):
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%dT%H:%M:%S')

# Crie um novo namespace para acessos
acesso_ns = Namespace('acessos', description='Operações relacionadas a acessos')

acesso_model = acesso_ns.model('Acesso', {
    'id': fields.Integer(readonly=True, description='ID da acesso'),
    'id_usuario': fields.Integer(required=True, description='ID do usuário'),
    'data_acesso': fields.DateTime(required=True, description='Data do acesso'),
    'caminho': fields.String(required=True, description='Caminho acessado'),
})

@acesso_ns.route('/')
class TodosAcessos(Resource):
    @acesso_ns.doc('listar_acessos')
    @acesso_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def get(self):
        '''Listar acessos'''
        acessos = Acesso.query.all()
        return [{'id': acesso.id, 'id_usuario': acesso.id_usuario, 'data_acesso': serialize_datetime(acesso.data_acesso), 'caminho': acesso.caminho} for acesso in acessos], 200
    
    @acesso_ns.doc('criar_registro_acesso')
    @acesso_ns.expect(acesso_model)
    def post(self):
        '''Criar um novo registro de acesso'''
        novo_acesso = acesso_ns.payload
        if 'login' in novo_acesso['caminho']:
            return {}, 201
        acesso = Acesso(
            id_usuario=novo_acesso['id_usuario'],
            data_acesso=serialize_datetime(datetime.now()),
            caminho=novo_acesso['caminho']
        )
        db.session.add(acesso)
        db.session.commit()
        return {'id': acesso.id, 'id_usuario': acesso.id_usuario, 'data_acesso': serialize_datetime(acesso.data_acesso), 'caminho': acesso.caminho}, 201