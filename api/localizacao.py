from flask import request
from flask_restx import Namespace, Resource, fields

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

CIDADES = [
    {
        "id": 1,
        "nome": "São Paulo",
        "id_estado": 1,
    },
    {
        "id": 2,
        "nome": "Rio de Janeiro",
        "id_estado": 2,
    }
]

ESTADOS = [
    {
        "id": 1,
        "nome": "São Paulo",
        "sigla": "SP",
    },
    {
        "id": 2,
        "nome": "Rio de Janeiro",
        "sigla": "RJ",
    }
]

BAIRROS = [
    {
        "id": 1,
        "nome": "Morumbi",
        "id_cidade": 1,
    },
    {
        "id": 2,
        "nome": "Copacabana",
        "id_cidade": 2,
    }
]

@localizacao_ns.route('/cidades')
class LocalizacaoCidadeLista(Resource):
    @localizacao_ns.doc('localizacao_listar_cidades', params={'id_estado': 'Identificador único do estado'})
    def get(self):
        '''Listar todas as cidades por estado'''
        id_estado = request.args.get('id_estado', type=int)
        if id_estado:
            return [cidade for cidade in CIDADES if cidade['id_estado'] == id_estado]
        else:
            return CIDADES
@localizacao_ns.route('/cidades/<int:id>')
@localizacao_ns.response(404, 'Cidade não encontrada')
@localizacao_ns.param('id', 'O identificador da cidade')
class Cidade(Resource):
    @localizacao_ns.doc('obter_cidade')
    def get(self, id):
        '''Obter uma cidade pelo identificador'''
        for cidade in CIDADES:
            if cidade['id'] == id:
                return cidade
        localizacao_ns.abort(404, f"Cidade {id} não encontrada")

@localizacao_ns.route('/estados')
class LocalizacaoEstadoLista(Resource):
    @localizacao_ns.doc('localizacao_listar_estados')
    def get(self):
        '''Listar todos os estados'''
        return ESTADOS
@localizacao_ns.route('/estados/<int:id>')
@localizacao_ns.response(404, 'Estado não encontrada')
@localizacao_ns.param('id', 'O identificador do estado')
class Estado(Resource):
    @localizacao_ns.doc('obter_estado')
    def get(self, id):
        '''Obter um estado pelo identificador'''
        for estado in ESTADOS:
            if estado['id'] == id:
                return estado
        localizacao_ns.abort(404, f"Estado {id} não encontrado")

@localizacao_ns.route('/bairros')
class LocalizacaoBairroLista(Resource):
    @localizacao_ns.doc('localizacao_listar_bairros', params={'id_cidade': 'Identificador único da cidade'})
    def get(self):
        '''Listar todos os bairros por cidade'''
        id_cidade = request.args.get('id_cidade', type=int)
        if id_cidade:
            return [bairro for bairro in BAIRROS if bairro['id_cidade'] == id_cidade]
        else:
            return BAIRROS
@localizacao_ns.route('/bairros/<int:id>')
@localizacao_ns.response(404, 'Bairro não encontrada')
@localizacao_ns.param('id', 'O identificador do bairro')
class Estado(Resource):
    @localizacao_ns.doc('obter_bairro')
    def get(self, id):
        '''Obter um bairro pelo identificador'''
        for bairro in BAIRROS:
            if bairro['id'] == id:
                return bairro
        localizacao_ns.abort(404, f"Bairro {id} não encontrado")