from config import db

class Imovel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

class TipoImovel(db.Model):
    __tablename__ = 'tipos_imoveis'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_imovel = db.Column(db.Integer, nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    valor_avaliacao = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date, nullable=False)

class FotosImovel(db.Model):
    __tablename__ = 'fotos_imovel'

    id = db.Column(db.Integer, primary_key=True)
    id_imovel = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.String(255), nullable=False)