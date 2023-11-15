from config import db

class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    telas = db.Column(db.String(255), nullable=False)

class Tela(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    caminho = db.Column(db.String(255), nullable=False)