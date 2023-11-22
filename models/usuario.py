from config import db
from flask_login import UserMixin


class Usuario(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    id_perfil = db.Column(db.Integer, nullable=False)
    data_cadastro = db.Column(db.DateTime, nullable=False)

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_imovel = db.Column(db.Integer, db.ForeignKey('imovel.id', ondelete='CASCADE'), nullable=False)
    imovel = db.relationship('Imovel', back_populates='favoritos')

