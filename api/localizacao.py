from flask import request
from flask_restx import Namespace, Resource, fields
from models.localizacao import Cidade, Estado, Bairro
from config import db

localizacao_ns = Namespace('localizacao', description='Operações de localização')

cidade_model = localizacao_ns.model('Cidade', {
    'id': fields.Integer(readOnly=True, description='Identificador único da cidade'),
    'nome': fields.String(required=True, description='Nome da cidade'),
    'id_estado': fields.Integer(required=True, description='Identificador do estado ao qual a cidade pertence'),
})

estado_model = localizacao_ns.model('Estado', {
    'id': fields.Integer(readOnly=True, description='Identificador único do estado'),
    'nome': fields.String(required=True, description='Nome do estado'),
    'sigla': fields.String(required=True, description='Sigla do estado'),
})

bairro_model = localizacao_ns.model('Bairro', {
    'id': fields.Integer(readOnly=True, description='Identificador único do estado'),
    'nome': fields.String(required=True, description='Nome do estado'),
    'id_cidade': fields.Integer(required=True, description='Identificador da cidade ao qual o bairro pertence'),
})

@localizacao_ns.route('/cidades')
class LocalizacaoCidadeLista(Resource):
    @localizacao_ns.doc('localizacao_listar_cidades', params={'id_estado': 'Identificador único do estado'})
    def get(self):
        '''Listar todas as cidades por estado'''
        id_estado = request.args.get('id_estado', type=int)
        if id_estado:
            cidades = Cidade.query.filter_by(id_estado=id_estado).all()
            return [{'id': cidade.id, 'nome': cidade.nome, 'id_estado': cidade.id_estado} for cidade in cidades]
        else:
            cidades = Cidade.query.all()
            return [{'id': cidade.id, 'nome': cidade.nome, 'id_estado': cidade.id_estado} for cidade in cidades]

@localizacao_ns.route('/cidades/<int:id>')
@localizacao_ns.response(404, 'Cidade não encontrada')
@localizacao_ns.param('id', 'O identificador da cidade')
class LocalizacaoCidade(Resource):
    @localizacao_ns.doc('obter_cidade')
    def get(self, id):
        '''Obter uma cidade pelo identificador'''
        cidade = Cidade.query.get(id)
        if cidade:
            return {'id': cidade.id, 'nome': cidade.nome, 'id_estado': cidade.id_estado}
        else:
            localizacao_ns.abort(404, f"Cidade {id} não encontrada")

@localizacao_ns.route('/estados')
class LocalizacaoEstadoLista(Resource):
    @localizacao_ns.doc('localizacao_listar_estados')
    def get(self):
        '''Listar todos os estados'''
        estados = Estado.query.all()
        return [{'id': estado.id, 'nome': estado.nome, 'sigla': estado.sigla} for estado in estados]

@localizacao_ns.route('/estados/<int:id>')
@localizacao_ns.response(404, 'Estado não encontrada')
@localizacao_ns.param('id', 'O identificador do estado')
class LocalizacaoEstado(Resource):
    @localizacao_ns.doc('obter_estado')
    def get(self, id):
        '''Obter um estado pelo identificador'''
        estado = Estado.query.get(id)
        if estado:
            return {'id': estado.id, 'nome': estado.nome, 'sigla': estado.sigla}
        else:
            localizacao_ns.abort(404, f"Estado {id} não encontrado")

@localizacao_ns.route('/bairros')
class LocalizacaoBairroLista(Resource):
    @localizacao_ns.doc('localizacao_listar_bairros', params={'id_cidade': 'Identificador único da cidade'})
    def get(self):
        '''Listar todos os bairros por cidade'''
        id_cidade = request.args.get('id_cidade', type=int)
        if id_cidade:
            bairros = Bairro.query.filter_by(id_cidade=id_cidade).all()
            return [{'id': bairro.id, 'nome': bairro.nome, 'id_cidade': bairro.id_cidade} for bairro in bairros]
        else:
            bairros = Bairro.query.all()
            return [{'id': bairro.id, 'nome': bairro.nome, 'id_cidade': bairro.id_cidade} for bairro in bairros]

@localizacao_ns.route('/bairros/<int:id>')
@localizacao_ns.response(404, 'Bairro não encontrada')
@localizacao_ns.param('id', 'O identificador do bairro')
class LocalizacaoBairro(Resource):
    @localizacao_ns.doc('obter_bairro')
    def get(self, id):
        '''Obter um bairro pelo identificador'''
        bairro = Bairro.query.get(id)
        if bairro:
            return {'id': bairro.id, 'nome': bairro.nome, 'id_cidade': bairro.id_cidade}
        else:
            localizacao_ns.abort(404, f"Bairro {id} não encontrado")