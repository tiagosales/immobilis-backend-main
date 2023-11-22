from flask import request
from flask_restx import Namespace, Resource, fields
from models.admin import Perfil, Tela
from models.usuario import Favorito,Usuario
from .utils import perfil_requerido
from datetime import datetime
from app import db,bcrypt

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

favorito_model = usuario_ns.model('Favorito', {
    'id': fields.Integer(readOnly=True, description='Identificador único do favorito'),
    'id_usuario': fields.Integer(required=True, description='Identificador do usuário'),
    'id_imovel': fields.Integer(required=True, description='Identificador do imóvel'),
})

# Função para serializar objetos datetime
def serialize_datetime(dt):
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


@usuario_ns.route('')

class ListaDeUsuarios(Resource):
    @usuario_ns.doc('listar_usuarios')
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def get(self):
        '''Listar todos os usuários'''
        usuarios = db.session.query(Usuario).all() 
        return [{'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email,
                 'senha': usuario.senha, 'id_perfil': usuario.id_perfil,
                 'data_cadastro': serialize_datetime(usuario.data_cadastro)} for usuario in usuarios]

    @usuario_ns.doc('criar_usuario')
    @usuario_ns.expect(user_model)
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def post(self):
        '''Criar um novo usuário'''
        novo_usuario = request.json
        novo_usuario['data_cadastro'] = serialize_datetime(datetime.now())
        novo_usuario['senha'] = bcrypt.generate_password_hash(novo_usuario['senha']).decode('utf-8')
        
        usuario = Usuario(**novo_usuario)
        db.session.add(usuario)
        db.session.commit()
        
        return {'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email,
                'senha': usuario.senha, 'id_perfil': usuario.id_perfil,
                'data_cadastro': serialize_datetime(usuario.data_cadastro)}, 201

@usuario_ns.route('/<int:id>')
@usuario_ns.response(404, 'Usuário não encontrado')
@usuario_ns.param('id', 'O identificador do usuário')
class UsuarioAPI(Resource):
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def get(self, id):
        '''Obter um usuário pelo identificador'''
        usuario = db.session.query(Usuario).filter_by(id=id).first()
        
        if not usuario:
            usuario_ns.abort(404, f"Usuário {id} não encontrado")
        
        return {'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email,
                'senha': usuario.senha, 'id_perfil': usuario.id_perfil,
                'data_cadastro': serialize_datetime(usuario.data_cadastro)}

    @usuario_ns.doc('update_user')
    @usuario_ns.expect(user_model)
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def put(self, id):
        '''Atualize um usuário pelo id'''
        user_data = request.json
        usuario = db.session.query(Usuario).filter_by(id=id).first()
        
        if not usuario:
            usuario_ns.abort(404, f"Usuário {id} não encontrado")
        
        usuario.nome = user_data['nome']
        usuario.email = user_data['email']
        usuario.id_perfil = user_data['id_perfil']
        if user_data['senha'] != '':
            usuario.senha=bcrypt.generate_password_hash(user_data['senha']).decode('utf-8')
        db.session.commit()
        
        return {'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email,
                'senha': usuario.senha, 'id_perfil': usuario.id_perfil,
                'data_cadastro': serialize_datetime(usuario.data_cadastro)}
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    @usuario_ns.doc('delete_user')
    def delete(self, id):
        '''Exclua um usuário pelo id'''
        usuario = db.session.query(Usuario).filter_by(id=id).first() 
        
        if not usuario:
            usuario_ns.abort(404, f"Usuário {id} não encontrado")
        
        db.session.delete(usuario)
        db.session.commit()
        
        return '', 204

@usuario_ns.route('/<int:id>/favoritos')
@usuario_ns.response(404, 'Usuário não encontrado')
@usuario_ns.param('id', 'O identificador do usuário')

class FavoritosUsuario(Resource):
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['1','2','3'])
    def get(self, id):
        '''Listar imóveis favoritos do usuário'''
        favoritos = db.session.query(Favorito).filter_by(id_usuario=id).all()  
        
        favoritos_tmp = [{'id': favorito.id, 'id_usuario': favorito.id_usuario, 'id_imovel': favorito.id_imovel} for favorito in favoritos]
        return favoritos_tmp

    @usuario_ns.doc('inserir_favorito_usuario')
    @usuario_ns.expect(favorito_model)
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['1','2','3'])
    def post(self, id):
        '''Criar/Favoritar imóvel'''
        novo_favorito = request.json
        novo_favorito['id_usuario'] = id 
        favorito = Favorito(**novo_favorito)  
        db.session.add(favorito)
        db.session.commit()
        
        return {'id': favorito.id, 'id_usuario': favorito.id_usuario, 'id_imovel': favorito.id_imovel}, 201
    
@usuario_ns.route('/<int:id>/favoritos/<int:id_imovel>')
@usuario_ns.response(404, 'Usuário não encontrado')
@usuario_ns.param('id', 'O identificador do usuário')
@usuario_ns.param('id_imovel', 'O identificador do imovel')

class FavoritoUsuario(Resource):
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['1','2','3'])
    def delete(self, id, id_imovel):
        '''Apagar favorito'''
        favorito = db.session.query(Favorito).filter_by(id_usuario=id, id_imovel=id_imovel).first() 
        
        if not favorito:
            usuario_ns.abort(404, f"Imóvel favorito {id_imovel} não encontrado para o usuário {id}")
        
        db.session.delete(favorito)
        db.session.commit()
        
        return '', 204
    
@usuario_ns.route('/<int:id>/telas-perfil')
@usuario_ns.response(404, 'Usuário não encontrado')
@usuario_ns.param('id', 'O identificador do usuário')
class TelasPerfil(Resource):
    @usuario_ns.doc(security='Bearer')
    @perfil_requerido(['1','2','3'])
    def get(self, id):
        '''Listar telas do usuário'''
        usuario = db.session.query(Usuario).filter_by(id=id).first()  # Substitua "Usuario" pelo seu modelo de usuário
        
        if not usuario:
            usuario_ns.abort(404, f"Usuário {id} não encontrado")
        
        perfil = db.session.query(Perfil).order_by(Perfil.id).filter_by(id=usuario.id_perfil).first()  
        perfiltelas = perfil.telas.strip('{}').split(',')  
        telas = db.session.query(Tela).order_by(Tela.id).filter(Tela.id.in_(perfiltelas))
        telasperfil_tmp = [{'nome': tela.nome, 'caminho': tela.caminho} for tela in telas]
        
        return telasperfil_tmp
