from config import db

class Imovel(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    id_cidade = db.Column(db.Integer, nullable=False)
    id_estado = db.Column(db.Integer, nullable=False)
    id_bairro = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    id_tipo = db.Column(db.Integer, nullable=False)
    quartos = db.Column(db.Integer, nullable=False)
    banheiros = db.Column(db.Integer, nullable=False)
    suites = db.Column(db.Integer, nullable=False)
    vagas_garagem = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    foto = db.Column(db.String(255), nullable=False)
    modalidade = db.Column(db.String(50), nullable=False)
    id_usuario = db.Column(db.Integer, nullable=False)
    favoritos = db.relationship('Favorito', back_populates='imovel', cascade='all, delete-orphan')
    fotos = db.relationship('FotosImovel', back_populates='imovel', cascade='all, delete-orphan')



class TipoImovel(db.Model):
    __tablename__ = 'tipos_imoveis'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_imovel = db.Column(db.Integer, nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    valor_avaliacao = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date, nullable=False)

class FotosImovel(db.Model):
    __tablename__ = 'fotos_imovel'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_imovel = db.Column(db.Integer,db.ForeignKey('imovel.id', ondelete='CASCADE'), nullable=False)
    foto = db.Column(db.String(255), nullable=False)
    imovel = db.relationship('Imovel', back_populates='fotos')
