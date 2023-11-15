from flask import request
from api.usuario import Favorito
from flask_restx import Namespace, Resource, fields
from models.imovel import Imovel as ImovelModel, TipoImovel as TipoImovelModel, Comentario as ComentarioModel, FotosImovel as FotosImovelModel
from config import db
from datetime import datetime

imovel_ns = Namespace('imoveis', description='Operações de imóveis')

imovel_model = imovel_ns.model('Imovel', {
    'id': fields.Integer(readOnly=True, description='Identificador único do imóvel'),
    'titulo': fields.String(required=True, description='Título do imóvel'),
    'descricao': fields.String(required=True, description='Descrição do imóvel'),
    'endereco': fields.String(required=True, description='Endereço do imóvel'),
    'id_cidade': fields.Integer(required=True, description='Identificador da cidade do imóvel'),
    'id_estado': fields.Integer(required=True, description='Identificador do estado do imóvel'),
    'id_bairro': fields.Integer(required=True, description='Identificador do bairro do imóvel'),
    'preco': fields.Float(required=True, description='Preço do imóvel'),
    'id_tipo': fields.Integer(required=True, description='Identificador do tipo do imóvel'),
    'quartos': fields.Integer(required=True, description='Número de quartos do imóvel'),
    'banheiros': fields.Integer(required=True, description='Número de banheiros do imóvel'),
    'suites': fields.Integer(required=True, description='Número de suítes do imóvel'),
    'vagas_garagem': fields.Integer(required=True, description='Número de vagas de garagem do imóvel'),
    'area': fields.Float(required=True, description='Área do imóvel'),
    'foto': fields.String(required=True, description='Endereço da imagem'),
    'modalidade': fields.String(required=True, description='Modalidade Compra ou Aluguel'),
    'id_usuario': fields.Integer(required=True, description='Identificador do usuário que cadastrou o imóvel'),
})

tipo_imovel_model = imovel_ns.model('TipoImovel', {
    'id': fields.Integer(readOnly=True, description='Identificador único do tipo de imóvel'),
    'nome': fields.String(required=True, description='Nome do tipo de imóvel'),
})

comentario_model = imovel_ns.model('Comentario',{
     'id': fields.Integer(readOnly=True, description='Identificador único do comentário'),
     'id_usuario': fields.Integer(required=True, description='Identificador do usuário'),
     'id_imovel': fields.Integer(required=True, description='Identificador do imóvel'),
     'texto': fields.String(required=True, description='Descrição do comentário'),
     'valor_avaliacao': fields.Integer(required=True, description='Valor de avaliação do usuário'),
     'data': fields.Date(required=True, description='Data de cadastro do comentário'),
})

fotosimovel_model = imovel_ns.model('FotosImovel',{
     'id': fields.Integer(readOnly=True, description='Identificador único da foto do imóvel'),
     'id_imovel': fields.Integer(required=True, description='Identificador do imóvel'),
     'foto': fields.String(required=True, description='URL foto imóvel'),
})

def serialize_datetime(dt):
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%dT%H:%M:%S')

@imovel_ns.route('')
class ListaDeImoveis(Resource):
    @imovel_ns.doc('listar_imoveis')
    @imovel_ns.doc(params={'modalidade': 'Modalidade Compra ou Aluguel', 
                             'id_estado': 'Localização (estado)',
                             'id_cidade': 'Localização (cidade)',
                             'id_bairro': 'Localização (bairro)',
                             'quartos': 'Número de quartos',
                             'banheiros': 'Número de banheiros',
                             'vagas_garagem': 'Número de vagas de garagem',
                             'suites': 'Número de suítes',
                             'area': 'Área do imóvel',
                             'id_tipo': 'Tipo de imóvel',
                             'preco_min': 'Preço mínimo',
                             'preco_max': 'Preço máximo',
                             'favoritados': 'Imóveis favoritados',
                             'usuario': 'Identificador do usuário'})
    def get(self):
        '''Listar todos os imóveis ou buscar com base nos parâmetros fornecidos'''
        modalidade = request.args.get('modalidade', None)
        id_estado = request.args.get('id_estado', None)
        id_cidade = request.args.get('id_cidade', None)
        id_bairro = request.args.get('id_bairro', None)
        quartos = request.args.get('quartos', None)
        banheiros = request.args.get('banheiros', None)
        vagas_garagem = request.args.get('vagas_garagem', None)
        suites = request.args.get('suites', None)
        area = request.args.get('area', None)
        id_tipo = request.args.get('id_tipo', None)
        preco_min = request.args.get('preco_min', None)
        preco_max = request.args.get('preco_max', None)
        favoritos = request.args.get('favoritos', None)
        usuario = request.args.get('usuario', None)

        # Se nenhum parâmetro de busca for fornecido, retorne todos os imóveis
        if not any([modalidade, id_estado,id_cidade, id_bairro, quartos,banheiros,vagas_garagem,suites,area, id_tipo, preco_min, preco_max]):
            imoveis = ImovelModel.query.all()
            imoveis_data = [{'id': imovel.id,
                             'titulo': imovel.titulo,
                             'descricao': imovel.descricao,
                             'endereco': imovel.endereco,
                             'id_cidade': imovel.id_cidade,
                             'id_estado': imovel.id_estado,
                             'id_bairro': imovel.id_bairro,
                             'preco': imovel.preco,
                             'id_tipo': imovel.id_tipo,
                             'quartos': imovel.quartos,
                             'banheiros': imovel.banheiros,
                             'suites': imovel.suites,
                             'vagas_garagem': imovel.vagas_garagem,
                             'area': imovel.area,
                             'foto': imovel.foto,
                             'modalidade': imovel.modalidade,
                             'id_usuario': imovel.id_usuario}
                            for imovel in imoveis]
            return imoveis_data

        filtered_properties = []
        query = ImovelModel.query

        if modalidade:
            query = query.filter(ImovelModel.modalidade.ilike(f"%{modalidade}%"))

        if id_estado:
            try:
                id_estado = int(id_estado)
                query = query.filter(ImovelModel.id_estado == id_estado)
            except ValueError:
                pass

        if id_cidade:
            try:
                id_cidade = int(id_cidade)
                query = query.filter(ImovelModel.id_cidade == id_cidade)
            except ValueError:
                pass

        if id_bairro:
            try:
                id_bairro = int(id_bairro)
                query = query.filter(ImovelModel.id_bairro == id_bairro)
            except ValueError:
                pass

        if quartos and quartos != 'Todos':
            query = query.filter(ImovelModel.quartos == int(quartos))

        if banheiros and banheiros != 'Todos':
            query = query.filter(ImovelModel.banheiros == int(banheiros))

        if vagas_garagem and vagas_garagem != 'Todos':
            query = query.filter(ImovelModel.vagas_garagem == int(vagas_garagem))

        if suites and suites != 'Todos':
            query = query.filter(ImovelModel.suites == int(suites))

        if id_tipo and id_tipo != 'Todos':
            query = query.filter(ImovelModel.id_tipo == int(id_tipo))

        if preco_min:
            query = query.filter(ImovelModel.preco >= float(preco_min))

        if preco_max:
            query = query.filter(ImovelModel.preco <= float(preco_max))

        if favoritos and favoritos == 'true':
            favoritos_imoveis = Favorito.query.filter(Favorito.id_usuario == int(usuario)).all()
            favoritos_ids = [favorito.id_imovel for favorito in favoritos_imoveis]
            query = query.filter(ImovelModel.id.in_(favoritos_ids))

        imoveis = query.all()
        imoveis_data = [{'id': imovel.id,
                         'titulo': imovel.titulo,
                         'descricao': imovel.descricao,
                         'endereco': imovel.endereco,
                         'id_cidade': imovel.id_cidade,
                         'id_estado': imovel.id_estado,
                         'id_bairro': imovel.id_bairro,
                         'preco': imovel.preco,
                         'id_tipo': imovel.id_tipo,
                         'quartos': imovel.quartos,
                         'banheiros': imovel.banheiros,
                         'suites': imovel.suites,
                         'vagas_garagem': imovel.vagas_garagem,
                         'area': imovel.area,
                         'foto': imovel.foto,
                         'modalidade': imovel.modalidade,
                         'id_usuario': imovel.id_usuario}
                        for imovel in imoveis]

        return imoveis_data

    @imovel_ns.doc('criar_imovel')
    @imovel_ns.expect(imovel_model)
    def post(self):
        '''Criar um novo imóvel'''
        novo_imovel_data = request.json
        novo_imovel = ImovelModel(**novo_imovel_data)
        db.session.add(novo_imovel)
        db.session.commit()
        return {
            'id': novo_imovel.id,
            'titulo': novo_imovel.titulo,
            'descricao': novo_imovel.descricao,
            'endereco': novo_imovel.endereco,
            'id_cidade': novo_imovel.id_cidade,
            'id_estado': novo_imovel.id_estado,
            'id_bairro': novo_imovel.id_bairro,
            'preco': novo_imovel.preco,
            'id_tipo': novo_imovel.id_tipo,
            'quartos': novo_imovel.quartos,
            'banheiros': novo_imovel.banheiros,
            'suites': novo_imovel.suites,
            'vagas_garagem': novo_imovel.vagas_garagem,
            'area': novo_imovel.area,
            'foto': novo_imovel.foto,
            'modalidade': novo_imovel.modalidade,
            'id_usuario': novo_imovel.id_usuario
        }, 201


@imovel_ns.route('/<int:id>')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')
class Imovel(Resource):
    @imovel_ns.doc('obter_imovel')
    def get(self, id):
        '''Obter um imóvel pelo identificador'''
        imovel = ImovelModel.query.get(id)
        if not imovel:
            imovel_ns.abort(404, f"Imóvel {id} não encontrado")
        return {
            'id': imovel.id,
            'titulo': imovel.titulo,
            'descricao': imovel.descricao,
            'endereco': imovel.endereco,
            'id_cidade': imovel.id_cidade,
            'id_estado': imovel.id_estado,
            'id_bairro': imovel.id_bairro,
            'preco': imovel.preco,
            'id_tipo': imovel.id_tipo,
            'quartos': imovel.quartos,
            'banheiros': imovel.banheiros,
            'suites': imovel.suites,
            'vagas_garagem': imovel.vagas_garagem,
            'area': imovel.area,
            'foto': imovel.foto,
            'modalidade': imovel.modalidade,
            'id_usuario': imovel.id_usuario
        }

    @imovel_ns.doc('atualizar_imovel')
    @imovel_ns.expect(imovel_model)
    def put(self, id):
        '''Atualizar um imóvel pelo id'''
        imovel = ImovelModel.query.get(id)
        if not imovel:
            imovel_ns.abort(404, f"Imóvel {id} não encontrado")

        imovel_data = request.json
        for key, value in imovel_data.items():
            setattr(imovel, key, value)

        db.session.commit()

        return {
            'id': imovel.id,
            'titulo': imovel.titulo,
            'descricao': imovel.descricao,
            'endereco': imovel.endereco,
            'id_cidade': imovel.id_cidade,
            'id_estado': imovel.id_estado,
            'id_bairro': imovel.id_bairro,
            'preco': imovel.preco,
            'id_tipo': imovel.id_tipo,
            'quartos': imovel.quartos,
            'banheiros': imovel.banheiros,
            'suites': imovel.suites,
            'vagas_garagem': imovel.vagas_garagem,
            'area': imovel.area,
            'foto': imovel.foto,
            'modalidade': imovel.modalidade,
            'id_usuario': imovel.id_usuario
        }

    @imovel_ns.doc('excluir_imovel')
    def delete(self, id):
        '''Excluir um imóvel pelo id'''
        imovel = ImovelModel.query.get(id)
        if not imovel:
            imovel_ns.abort(404, f"Imóvel {id} não encontrado")

        db.session.delete(imovel)
        db.session.commit()

        return '', 204
@imovel_ns.route('/<int:id>/comentarios')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')
class ComentariosImovel(Resource):
    @imovel_ns.doc('listar_comentarios_imovel')
    def get(self, id):
        '''Listar comentários do imóvel'''
        comentarios = ComentarioModel.query.filter_by(id_imovel=id).all()
        comentarios_data = [{
            'id': comentario.id,
            'id_usuario': comentario.id_usuario,
            'id_imovel': comentario.id_imovel,
            'texto': comentario.texto,
            'valor_avaliacao': comentario.valor_avaliacao,
            'data': serialize_datetime(comentario.data)
        } for comentario in comentarios]
        return comentarios_data

    @imovel_ns.doc('inserir_comentario_usuario')
    @imovel_ns.expect(comentario_model)
    def post(self, id):
        '''Criar comentário sobre o imóvel'''
        novo_comentario_data = request.json
        novo_comentario = ComentarioModel(
            id_usuario=novo_comentario_data['id_usuario'],
            id_imovel=id,
            texto=novo_comentario_data['texto'],
            valor_avaliacao=novo_comentario_data['valor_avaliacao'],
            data=serialize_datetime(datetime.now())
        )
        db.session.add(novo_comentario)
        db.session.commit()
        return {
            'id': novo_comentario.id,
            'id_usuario': novo_comentario.id_usuario,
            'id_imovel': novo_comentario.id_imovel,
            'texto': novo_comentario.texto,
            'valor_avaliacao': novo_comentario.valor_avaliacao,
            'data': serialize_datetime(novo_comentario.data)
        }, 201

@imovel_ns.route('/<int:id>/avaliacao')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')
class AvaliacaoImovel(Resource):
    @imovel_ns.doc('listar_media_avaliacoes_imovel')
    def get(self, id):
        '''Média de avaliações do imóvel'''
        comentarios = ComentarioModel.query.filter_by(id_imovel=id).all()
        total_avaliacoes = sum([comentario.valor_avaliacao for comentario in comentarios])
        media_avaliacoes = total_avaliacoes / len(comentarios) if comentarios else 0
        return {'mediaAvaliacoes': round(media_avaliacoes, 1)}

@imovel_ns.route('/<int:id>/fotosimovel')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')
class FotosImovel(Resource):
    @imovel_ns.doc('listar_fotos_imovel')
    def get(self, id):
        '''Listar fotos do imóvel'''
        fotos = FotosImovelModel.query.filter_by(id_imovel=id).all()
        fotos_data = [{
            'id': foto.id,
            'id_imovel': foto.id_imovel,
            'foto': foto.foto
        } for foto in fotos]
        return fotos_data

    @imovel_ns.doc('inserir_fotos_imovel')
    @imovel_ns.expect(fotosimovel_model)
    def post(self, id):
        '''Adicionar fotos do imóvel'''
        nova_foto_data = request.json
        nova_foto = FotosImovelModel(
            id_imovel=id,
            foto=nova_foto_data['foto']
        )
        db.session.add(nova_foto)
        db.session.commit()
        return {
            'id': nova_foto.id,
            'id_imovel': nova_foto.id_imovel,
            'foto': nova_foto.foto
        }, 201

@imovel_ns.route('/<int:id>/fotosimovel/<int:id_foto>')
@imovel_ns.response(404, 'Imóvel ou foto não encontrada')
@imovel_ns.param('id', 'O identificador do imóvel')
@imovel_ns.param('id_foto', 'O identificador da foto')
class FotosImovel(Resource):
    @imovel_ns.doc('apagar_foto_imovel')
    def delete(self, id, id_foto):
        '''Excluir uma foto pelo id'''
        foto = FotosImovelModel.query.filter_by(id_imovel=id, id=id_foto).first()
        if not foto:
            imovel_ns.abort(404, f"Foto {id_foto} não encontrada para o imóvel {id}")
        db.session.delete(foto)
        db.session.commit()
        return '', 204

@imovel_ns.route('/tipos-imoveis')
class AdminTipoImovelLista(Resource):
    @imovel_ns.doc('listar_tipos_imoveis')
    def get(self):
        '''Listar todos os tipos de imóveis'''
        tipos_imoveis = TipoImovelModel.query.all()
        tipos_imoveis_data = [{
            'id': tipo_imovel.id,
            'nome': tipo_imovel.nome
        } for tipo_imovel in tipos_imoveis]
        return tipos_imoveis_data

    @imovel_ns.doc('criar_tipo_imovel')
    @imovel_ns.expect(tipo_imovel_model)
    def post(self):
        '''Criar um novo tipo de imóvel '''
        novo_tipo_imovel_data = request.json
        novo_tipo_imovel = TipoImovelModel(
            nome=novo_tipo_imovel_data['nome']
        )
        db.session.add(novo_tipo_imovel)
        db.session.commit()
        return {
            'id': novo_tipo_imovel.id,
            'nome': novo_tipo_imovel.nome
        }, 201

@imovel_ns.route('/tipos-imoveis/<int:id>')
@imovel_ns.response(404, 'Tipo de imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do tipo de imóvel')
class TipoImovel(Resource):
    @imovel_ns.doc('obter_tipo_imovel')
    def get(self, id):
        '''Obter um tipo de imóvel pelo identificador'''
        tipo_imovel = TipoImovelModel.query.get(id)
        if not tipo_imovel:
            imovel_ns.abort(404, f"Tipo de imóvel {id} não encontrado")
        return {
            'id': tipo_imovel.id,
            'nome': tipo_imovel.nome
        }

    @imovel_ns.doc('atualizar_tipo_imovel')
    @imovel_ns.expect(tipo_imovel_model)
    def put(self, id):
        '''Atualizar um tipo de imóvel pelo id '''
        tipo_imovel = TipoImovelModel.query.get(id)
        if not tipo_imovel:
            imovel_ns.abort(404, f"Tipo de imóvel {id} não encontrado")
        tipo_imovel_data = request.json
        tipo_imovel.nome = tipo_imovel_data['nome']
        db.session.commit()
        return {
            'id': tipo_imovel.id,
            'nome': tipo_imovel.nome
        }

    @imovel_ns.doc('excluir_tipo_imovel')
    def delete(self, id):
        '''Excluir um tipo de imóvel pelo id'''
        tipo_imovel = TipoImovelModel.query.get(id)
        if not tipo_imovel:
            imovel_ns.abort(404, f"Tipo de imóvel {id} não encontrado")
        db.session.delete(tipo_imovel)
        db.session.commit()
        return '', 204
    
@imovel_ns.route('/tipos-imoveis/<int:id>')
@imovel_ns.response(404, 'Tipo de imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do tipo de imóvel')
class TipoImovel(Resource):
    @imovel_ns.doc('excluir_tipo_imovel')
    def delete(self, id):
        '''Excluir um tipo de imóvel pelo id'''
        tipo_imovel = TipoImovelModel.query.get(id)
        if not tipo_imovel:
            imovel_ns.abort(404, f"Tipo de imóvel {id} não encontrado")
        db.session.delete(tipo_imovel)
        db.session.commit()
        return '', 204
