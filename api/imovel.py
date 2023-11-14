from flask import request
from api.usuario import Favorito
from flask_restx import Namespace, Resource, fields

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
    'id_usuario': fields.Integer(required=True, description='Identificador usuario que cadastrou o imovel'),
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
     'foto': fields.String(required=True, description='URL foto imovel'),
})

IMOVEIS = [
    {
        "id": 1001,
        "titulo": "Casa moderna",
        "descricao": "Casa moderna com 4 quartos e piscina",
        "endereco": "Rua das Flores, 123",
        "id_cidade": 1,
        "id_estado": 1,
        "id_bairro": 1,
        "preco": 750000,
        "id_tipo": 1,
        "quartos": 4,
        "banheiros": 3,
        "suites": 1,
        "vagas_garagem": 2,
        "area": 300,
	    "foto": "https://via.placeholder.com/150",
        "modalidade": "aluguel",
        "id_usuario": 1,
    },
    {
        "id": 1002,
        "titulo": "Apartamento de luxo",
        "descricao": "Apartamento de luxo com vista para o mar",
        "endereco": "Av. Beira Mar, 456",
        "id_cidade": 2,
        "id_estado": 2,
        "id_bairro": 2,
        "preco": 1500000,
        "id_tipo": 2,
        "quartos": 3,
        "banheiros": 2,
        "suites": 1,
        "vagas_garagem": 1,
        "area": 200,
	    "foto": "https://via.placeholder.com/150",
        "modalidade": "venda",
        "id_usuario": 2,
    }
]

TIPOS_IMOVEIS = [
    {
        "id": 1,
        "nome": "Casa",
    },
    {
        "id": 2,
        "nome": "Apartamento",
    }
]

COMENTARIOS = [
            {
                "id": 1,
                "id_usuario": 3,
                "id_imovel": 1001,
                "texto": "Ótimo imóvel! Recomendo!",
                "valor_avaliacao": "5",
                "data": "2022-10-02",
            },
            {
                "id": 1,
                "id_usuario": 5,
                "id_imovel": 1001,
                "texto": "Espaçoso e agradável!",
                "valor_avaliacao": "5",
                "data": "2022-11-02",
            },
            {
                "id": 2,
                "id_usuario": 4,
                "id_imovel": 1002,
                "texto": "Excelente localização!",
                "valor_avaliacao": "4",
                "data": "2022-05-02",
            },
        ]

FOTOSIMOVEL = [
            {
                "id": 1,
                "foto": "https://via.placeholder.com/150",
                "id_imovel": 1001,
            },{
                "id": 2,
                "foto": "https://via.placeholder.com/150",
                "id_imovel": 1002,
            },]

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
                             'suites': 'Número de vagas de garagem',
                             'area': 'Área do imóvel',
                             'id_tipo': 'Tipo de imóvel',
                             'preco_min': 'Preço mínimo',
                             'preco_max': 'Preço máximo',
                             'favoritados': 'Imóveis favoritados'})
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
        usuario = request.args.get('usuario',None)

        # Se nenhum parâmetro de busca for fornecido, retorne todos os imóveis
        if not any([modalidade, id_estado,id_cidade, id_bairro, quartos,banheiros,vagas_garagem,suites,area, id_tipo, preco_min, preco_max]):
            return IMOVEIS

        filtered_properties = IMOVEIS
        if modalidade:
            filtered_properties = [p for p in filtered_properties if modalidade.lower() in p['modalidade'].lower()]

        if id_estado:
            try:
                id_estado = int(id_estado)
                filtered_properties = [p for p in filtered_properties if p.get('id_estado') == int(id_estado)]
            except:
                pass
        if id_cidade:
            try:
                id_cidade = int(id_cidade)
                filtered_properties = [p for p in filtered_properties if p.get('id_cidade') == int(id_cidade)]
            except:
                pass
        if id_bairro:
            try:
                id_bairro = int(id_bairro)
                filtered_properties = [p for p in filtered_properties if p.get('id_bairro') == int(id_bairro)]
            except:
                pass

        if quartos:
            if quartos != 'Todos':
                filtered_properties = [p for p in filtered_properties if p.get('quartos') == int(quartos)]

        if banheiros:
            if banheiros != 'Todos':
                filtered_properties = [p for p in filtered_properties if p.get('banheiros') == int(banheiros)]

        if vagas_garagem:
            if vagas_garagem != 'Todos':   
                filtered_properties = [p for p in filtered_properties if p.get('vagas_garagem') == int(vagas_garagem)]

        if suites:
            if suites != 'Todos': 
                filtered_properties = [p for p in filtered_properties if p.get('suites') == int(suites)]


        if id_tipo:
            if id_tipo != 'Todos': 
                # Filtre os imóveis com base no tipo de imóvel
                filtered_properties = [p for p in filtered_properties if p.get('id_tipo') == int(id_tipo)]

        if preco_min or preco_max:
            # Filtre os imóveis com base no preço
            if preco_min:
                filtered_properties = [p for p in filtered_properties if p['preco'] >= float(preco_min)]
            if preco_max:
                filtered_properties = [p for p in filtered_properties if p['preco'] <= float(preco_max)]

        if favoritos:
            if favoritos == 'true':
                FAVORITOS=Favorito.query.all()
                favoritos_usuario = []
                for favorito in FAVORITOS:    
                    if int(favorito.id_usuario) == int(usuario):
                        favoritos_usuario.append(favorito.id_imovel)
                filtered_properties = [p for p in filtered_properties if p['id'] in favoritos_usuario ]

        return filtered_properties

    @imovel_ns.doc('criar_imovel')
    @imovel_ns.expect(imovel_model)
    def post(self):
        '''Criar um novo imóvel'''
        novo_imovel = request.json
        novo_imovel['id'] = len(IMOVEIS) + 1
        IMOVEIS.append(novo_imovel)
        return novo_imovel, 201

@imovel_ns.route('/<int:id>')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')
class Imovel(Resource):
    @imovel_ns.doc('obter_imovel')
    def get(self, id):
        '''Obter um imóvel pelo identificador'''
        for imovel in IMOVEIS:
            if imovel['id'] == id:
                return imovel
        imovel_ns.abort(404, f"Imóvel {id} não encontrado")

    @imovel_ns.doc('atualizar_imovel')
    @imovel_ns.expect(imovel_model)
    def put(self, id):
        '''Atualizar um imóvel pelo id'''
        imovel_para_atualizar = None
        for imovel in IMOVEIS:
            if imovel['id'] == id:
                imovel_para_atualizar = imovel
                break
        if not imovel_para_atualizar:
            imovel_ns.abort(404, f"Imóvel {id} não encontrado")
        imovel_data = request.json
        imovel_para_atualizar.update(imovel_data)
        return imovel_para_atualizar

    @imovel_ns.doc('excluir_imovel')
    def delete(self, id):
        '''Excluir um imóvel pelo id'''
        imovel_para_excluir = None
        for imovel in IMOVEIS:
            if imovel['id'] == id:
                imovel_para_excluir = imovel
                break
        if not imovel_para_excluir:
            imovel_ns.abort(404, f"Imóvel {id} não encontrado")
        IMOVEIS.remove(imovel_para_excluir)
        return '', 204


@imovel_ns.route('/<int:id>/comentarios')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')
class ComentariosImovel(Resource):
    @imovel_ns.doc('listar_comentarios_imovel')
    def get(self, id):
        '''Listar comentários do imóvel'''
        comentarios_tmp = []
        for comentario in COMENTARIOS:
            if comentario['id_imovel'] == id:
                comentarios_tmp.append(comentario)
        return comentarios_tmp
    @imovel_ns.doc('inserir_comentario_usuario')
    @imovel_ns.expect(comentario_model)
    def post(self,id):
        '''Criar comentário sobre o imóvel'''
        novo_comentario = request.json
        novo_comentario['id'] = len(COMENTARIOS) + 1
        novo_comentario['id_imovel'] = id
        COMENTARIOS.append(novo_comentario)
        return novo_comentario, 201

@imovel_ns.route('/<int:id>/avaliacao')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')
class AvaliacaoImovel(Resource):
    @imovel_ns.doc('listar_media_avaliacoes_imovel')
    def get(self, id):
        '''Media de avaliacoes do imóvel'''
        comentarios_tmp = []
        total = 0
        count = 0
        for comentario in COMENTARIOS:
            if int(comentario['valor_avaliacao']) > 0 and comentario['id_imovel'] == id:
                count = count + 1
                total = total + int(comentario['valor_avaliacao'])
        media = total / count
        return { "mediaAvaliacoes": round(media,1) }
    
@imovel_ns.route('/<int:id>/fotosimovel')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')

class FotosImovel(Resource):
    @imovel_ns.doc('listar_fotos_imovel')
    def get(self, id):
        '''Listar fotos do imóvel'''
        fotosimovel_tmp = []
        for fotoimovel in FOTOSIMOVEL:
            if fotoimovel['id_imovel'] == id:
                fotosimovel_tmp.append(fotoimovel)
        return fotosimovel_tmp
    @imovel_ns.doc('inserir_fotos_imovel')
    @imovel_ns.expect(fotosimovel_model)
    def post(self,id):
        '''Adicionar fotos do imóvel'''
        nova_fotoimovel = request.json
        nova_fotoimovel['id'] = len(FOTOSIMOVEL) + 1
        nova_fotoimovel['id_imovel'] = id
        FOTOSIMOVEL.append(nova_fotoimovel)
        return nova_fotoimovel, 201
    
@imovel_ns.route('/<int:id>/fotosimovel/<int:id_foto>')
@imovel_ns.response(404, 'Imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do imóvel')
@imovel_ns.param('id_foto', 'O identificador da foto')
class FotosImovel(Resource):
    @imovel_ns.doc('apagar_foto_imovel')
    def delete(self, id, id_foto):
        '''Exclua uma foto pelo id'''
        foto_para_apagar = None
        for foto in FOTOSIMOVEL:
            if foto['id_imovel'] == id and foto['id'] == id_foto:
                foto_para_apagar = foto
                break
        if not foto_para_apagar:
            imovel_ns.abort(404, f"Foto {id_foto} não encontrada para o imovel {id}")
        FOTOSIMOVEL.remove(foto_para_apagar)
        return '', 204
    
@imovel_ns.route('/tipos-imoveis')
class AdminTipoImovelLista(Resource):
    @imovel_ns.doc('listar_tipos_imoveis')
    def get(self):
        '''Listar todos os tipos de imóveis'''
        return TIPOS_IMOVEIS

    @imovel_ns.doc('criar_tipo_imovel')
    @imovel_ns.expect(tipo_imovel_model)
    def post(self):
        '''Criar um novo tipo de imóvel '''
        novo_tipo_imovel = request.json
        novo_tipo_imovel['id'] = len(TIPOS_IMOVEIS) + 1
        TIPOS_IMOVEIS.append(novo_tipo_imovel)
        return novo_tipo_imovel, 201

@imovel_ns.route('/tipos-imoveis/<int:id>')
@imovel_ns.response(404, 'Tipo de imóvel não encontrado')
@imovel_ns.param('id', 'O identificador do tipo de imóvel')
class TipoImovel(Resource):
    @imovel_ns.doc('obter_tipo_imovel')
    def get(self, id):
        '''Obter um tipo de imóvel pelo identificador'''
        for tipo_imovel in TIPOS_IMOVEIS:
            if tipo_imovel['id'] == id:
                return tipo_imovel
        imovel_ns.abort(404, f"Tipo de imóvel {id} não encontrado")

    @imovel_ns.doc('atualizar_tipo_imovel')
    @imovel_ns.expect(tipo_imovel_model)
    def put(self, id):
        '''Atualizar um tipo de imóvel pelo id '''
        tipo_imovel_to_update = None
        for tipo_imovel in TIPOS_IMOVEIS:
            if tipo_imovel['id'] == id:
                tipo_imovel_to_update = tipo_imovel
                break
        if not tipo_imovel_to_update:
            imovel_ns.abort(404, f"Tipo de imóvel {id} não encontrado")
        tipo_imovel_data = request.json
        tipo_imovel_to_update['nome'] = tipo_imovel_data['nome']
        return tipo_imovel_to_update

    @imovel_ns.doc('excluir_tipo_imovel')
    def delete(self, id):
        '''Excluir um tipo de imóvel pelo id'''
        tipo_imovel_to_delete = None
        for tipo_imovel in TIPOS_IMOVEIS:
            if tipo_imovel['id'] == id:
                tipo_imovel_to_delete = tipo_imovel
                break
        if not tipo_imovel_to_delete:
            imovel_ns.abort(404, f"Tipo de imóvel {id} não encontrado")
        TIPOS_IMOVEIS.remove(tipo_imovel_to_delete)
        return '', 204