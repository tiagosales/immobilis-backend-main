# admin.py

from flask import Flask, request
from flask_restx import Namespace, Resource, fields
from models.admin import Perfil, Tela
from config import db
from .utils import perfil_requerido

admin_ns = Namespace('admin', description='Operações de administração')

perfil_model = admin_ns.model('Perfil', {
    'id': fields.Integer(readOnly=True, description='Identificador único do perfil'),
    'nome': fields.String(required=True, description='Nome do perfil'),
    'descricao': fields.String(required=True, description='Descrição do perfil'),
    'telas': fields.String(required=True, description='Telas do perfil'),
})

tela_model = admin_ns.model('Tela', {
    'id': fields.Integer(readOnly=True, description='Identificador único da tela'),
    'nome': fields.String(required=True, description='Nome da tela'),
    'descricao': fields.String(required=True, description='Descrição da tela'),
    'caminho': fields.String(required=True, description='Caminho da tela na aplicação'),
})

@admin_ns.route('/perfis')
class AdminPerfilLista(Resource):
    @admin_ns.doc('admin_listar_perfis')
    @admin_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def get(self):
        '''Listar todos os perfis (para administradores)'''
        perfis = Perfil.query.order_by(Perfil.id).all()
        return [{'id': perfil.id, 'nome': perfil.nome, 'descricao': perfil.descricao, 'telas': perfil.telas} for perfil in perfis]

    @admin_ns.doc('admin_criar_perfil')
    @admin_ns.expect(perfil_model)
    @admin_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def post(self):
        '''Criar um novo perfil (para administradores)'''
        novo_perfil = request.json
        perfil = Perfil(nome=novo_perfil['nome'], descricao=novo_perfil['descricao'], telas=novo_perfil['telas'])
        db.session.add(perfil)
        db.session.commit()
        return {'id': perfil.id, 'nome': perfil.nome, 'descricao': perfil.descricao, 'telas': perfil.telas}, 201

@admin_ns.route('/perfis/<int:id>')
@admin_ns.response(404, 'Perfil não encontrado')
@admin_ns.param('id', 'O identificador do perfil')
class AdminPerfil(Resource):
    @admin_ns.doc('admin_obter_perfil')
    def get(self, id):
        '''Obter um perfil pelo identificador (para administradores)'''
        perfil = Perfil.query.get(id)
        if not perfil:
            admin_ns.abort(404, f"Perfil {id} não encontrado")
        return {'id': perfil.id, 'nome': perfil.nome, 'descricao': perfil.descricao, 'telas': perfil.telas}

    @admin_ns.doc('admin_atualizar_perfil')
    @admin_ns.expect(perfil_model)
    @admin_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def put(self, id):
        '''Atualizar um perfil pelo id (para administradores)'''
        perfil = Perfil.query.get(id)
        if not perfil:
            admin_ns.abort(404, f"Perfil {id} não encontrado")
        
        perfil_data = request.json
        perfil.nome = perfil_data['nome']
        perfil.descricao = perfil_data['descricao']
        perfil.telas = perfil_data['telas']
        db.session.commit()
        
        return {'id': perfil.id, 'nome': perfil.nome, 'descricao': perfil.descricao, 'telas': perfil.telas}

    @admin_ns.doc('admin_excluir_perfil')
    @admin_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def delete(self, id):
        '''Excluir um perfil pelo id (para administradores)'''
        perfil = Perfil.query.get(id)
        if not perfil:
            admin_ns.abort(404, f"Perfil {id} não encontrado")
        
        db.session.delete(perfil)
        db.session.commit()
        
        return '', 204

@admin_ns.route('/telas')
class AdminTelaLista(Resource):
    @admin_ns.doc('admin_listar_telas')
    def get(self):
        '''Listar todas as telas (para administradores)'''
        telas = Tela.query.order_by(Tela.id).all()
        return [{'id': tela.id, 'nome': tela.nome, 'descricao': tela.descricao, 'caminho': tela.caminho} for tela in telas]

    @admin_ns.doc('admin_criar_tela')
    @admin_ns.expect(tela_model)
    @admin_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def post(self):
        '''Criar uma nova tela (para administradores)'''
        nova_tela = request.json
        tela = Tela(nome=nova_tela['nome'], descricao=nova_tela['descricao'], caminho=nova_tela['caminho'])
        db.session.add(tela)
        db.session.commit()
        return {'id': tela.id, 'nome': tela.nome, 'descricao': tela.descricao, 'caminho': tela.caminho}, 201

@admin_ns.route('/telas/<int:id>')
@admin_ns.response(404, 'Tela não encontrada')
@admin_ns.param('id', 'O identificador da tela')
class AdminTela(Resource):
    @admin_ns.doc('admin_obter_tela')
    def get(self, id):
        '''Obter uma tela pelo identificador (para administradores)'''
        tela = Tela.query.get(id)
        if not tela:
            admin_ns.abort(404, f"Tela {id} não encontrada")
        return {'id': tela.id, 'nome': tela.nome, 'descricao': tela.descricao, 'caminho': tela.caminho}

    @admin_ns.doc('admin_atualizar_tela')
    @admin_ns.expect(tela_model)
    @admin_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def put(self, id):
        '''Atualizar uma tela pelo id (para administradores)'''
        tela = Tela.query.get(id)
        if not tela:
            admin_ns.abort(404, f"Tela {id} não encontrada")
        
        tela_data = request.json
        tela.nome = tela_data['nome']
        tela.descricao = tela_data['descricao']
        tela.caminho = tela_data['caminho']
        db.session.commit()
        
        return {'id': tela.id, 'nome': tela.nome, 'descricao': tela.descricao, 'caminho': tela.caminho}

    @admin_ns.doc('admin_excluir_tela')
    @admin_ns.doc(security='Bearer')
    @perfil_requerido(['2'])
    def delete(self, id):
        '''Excluir uma tela pelo id (para administradores)'''
        tela = Tela.query.get(id)
        if not tela:
            admin_ns.abort(404, f"Tela {id} não encontrada")
        
        db.session.delete(tela)
        db.session.commit()
        
        return '', 204
