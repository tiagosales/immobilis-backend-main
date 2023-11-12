from config import db

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    texto = db.Column(db.String(255), nullable=False)
    id_usuario_remetente = db.Column(db.Integer, nullable=False)
    id_usuario_destinatario = db.Column(db.Integer)
    nome = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    id_imovel = db.Column(db.Integer, nullable=False)
    