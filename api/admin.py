from flask import request
from flask_restx import Namespace, Resource, fields

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
    'caminho': fields.String(required=True, description='Código da tela na aplicação'),
})

TELAS = [{"id": 1, "nome": "Busca de Im\u00f3veis", "descricao": "Tela para busca de im\u00f3veis", "caminho": "/busca"}, 
         {"id": 2, "nome": "Gerenciar de Im\u00f3veis", "descricao": "Tela para gerenciamento de im\u00f3veis", "caminho": "/imoveis"}, 
         {"id": 3, "nome": "Gerenciar Usuarios", "descricao": "Tela para gerenciamento de usu\u00e1rios", "caminho": "/usuarios"}, 
         {"nome": "Gerenciar perfis", "descricao": "Tela para gerenciamento de perfis", "caminho": "/perfis", "id": 4}, 
         {"nome": "Gerenciar telas", "descricao": "Tela para gerenciamento de telas", "caminho": "/telas", "id": 5},
         {"nome": "Mensagens", "descricao": "Tela para gerenciamento de mensagens", "caminho": "/mensagens", "id": 6},
         {"nome": "Estatisticas", "descricao": "Tela para acompanhamento de estatisticas", "caminho": "/estatisticas", "id": 7},
         {"nome": "Gerenciar tipos de imoveis", "descricao": "Tela para gerenciamento de tipos de imoveis", "caminho": "/tiposimoveis", "id": 8},

         ]





PERFIS = [{"id": 1, "nome": "Cliente", "descricao": "Perfil de usu\u00e1rio b\u00e1sico logado", "telas": [1]}, 
          {"id": 2, "nome": "Administrador", "descricao": "Perfil com acesso total ao sistema", "telas": [1, 2, 3, 4, 5,6,7,8]}, 
          {"id": 3, "nome": "Corretor", "descricao": "Perfil com acesso limitado ao gerenciamento de im\u00f3veis", "telas": [1, 2,6]}
          ]




@admin_ns.route('/perfis')
class AdminPerfilLista(Resource):
    @admin_ns.doc('admin_listar_perfis')
    def get(self):
        '''Listar todos os perfis (para administradores)'''
        return PERFIS

    @admin_ns.doc('admin_criar_perfil')
    @admin_ns.expect(perfil_model)
    def post(self):
        '''Criar um novo perfil (para administradores)'''
        novo_perfil = request.json
        novo_perfil['id'] = len(PERFIS) + 1
        PERFIS.append(novo_perfil)
        return novo_perfil, 201

@admin_ns.route('/perfis/<int:id>')
@admin_ns.response(404, 'Perfil não encontrado')
@admin_ns.param('id', 'O identificador do perfil')
class AdminPerfil(Resource):
    @admin_ns.doc('admin_obter_perfil')
    def get(self, id):
        '''Obter um perfil pelo identificador (para administradores)'''
        for perfil in PERFIS:
            if perfil['id'] == id:
                return perfil
        admin_ns.abort(404, f"Perfil {id} não encontrado")

    @admin_ns.doc('admin_atualizar_perfil')
    @admin_ns.expect(perfil_model)
    def put(self, id):
        '''Atualizar um perfil pelo id (para administradores)'''
        perfil_to_update = None
        for perfil in PERFIS:
            if perfil['id'] == id:
                perfil_to_update = perfil
                break
        if not perfil_to_update:
            admin_ns.abort(404, f"Perfil {id} não encontrado")
        perfil_data = request.json
        perfil_to_update['nome'] = perfil_data['nome']
        perfil_to_update['descricao'] = perfil_data['descricao']
        perfil_to_update['telas'] = perfil_data['telas']
        return perfil_to_update

    @admin_ns.doc('admin_excluir_perfil')
    def delete(self, id):
        '''Excluir um perfil pelo id (para administradores)'''
        perfil_to_delete = None
        for perfil in PERFIS:
            if perfil['id'] == id:
                perfil_to_delete = perfil
                break
        if not perfil_to_delete:
            admin_ns.abort(404, f"Perfil {id} não encontrado")
        PERFIS.remove(perfil_to_delete)
        return '', 204

@admin_ns.route('/telas')
class AdminTelaLista(Resource):
    @admin_ns.doc('admin_listar_telas')
    def get(self):
        '''Listar todas as telas (para administradores)'''
        return TELAS

    @admin_ns.doc('admin_criar_tela')
    @admin_ns.expect(tela_model)
    def post(self):
        '''Criar uma nova tela (para administradores)'''
        nova_tela = request.json
        nova_tela['id'] = len(TELAS) + 1
        TELAS.append(nova_tela)
        return nova_tela, 201

@admin_ns.route('/telas/<int:id>')
@admin_ns.response(404, 'Tela não encontrada')
@admin_ns.param('id', 'O identificador da tela')
class AdminTela(Resource):
    @admin_ns.doc('admin_obter_tela')
    def get(self, id):
        '''Obter uma tela pelo identificador (para administradores)'''
        for tela in TELAS:
            if tela['id'] == id:
                return tela
        admin_ns.abort(404, f"Tela {id} não encontrada")

    @admin_ns.doc('admin_atualizar_tela')
    @admin_ns.expect(tela_model)
    def put(self, id):
        '''Atualizar uma tela pelo id (para administradores)'''
        tela_to_update = None
        for tela in TELAS:
            if tela['id'] == id:
                tela_to_update = tela
                break
        if not tela_to_update:
            admin_ns.abort(404, f"Tela {id} não encontrada")
        tela_data = request.json
        tela_to_update['nome'] = tela_data['nome']
        tela_to_update['descricao'] = tela_data['descricao']
        tela_to_update['caminho'] = tela_data['caminho']
        return tela_to_update

    @admin_ns.doc('admin_excluir_tela')
    def delete(self, id):
        '''Excluir uma tela pelo id (para administradores)'''
        tela_to_delete = None
        for tela in TELAS:
            if tela['id'] == id:
                tela_to_delete = tela
                break
        if not tela_to_delete:
            admin_ns.abort(404, f"Tela {id} não encontrada")
        TELAS.remove(tela_to_delete)
        return '', 204






