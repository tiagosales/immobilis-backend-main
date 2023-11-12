from config import db

class Acesso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    data_acesso = db.Column(db.DateTime, nullable=False)
    caminho = db.Column(db.String(255), nullable=False)