from config import db

class Cidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    id_estado = db.Column(db.Integer, nullable=False)

class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sigla = db.Column(db.String(2), nullable=False)

class Bairro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    id_cidade = db.Column(db.Integer, nullable=False)

#Dados de mock
'''-- Estados
INSERT INTO estado (id, nome, sigla) VALUES (1, 'São Paulo', 'SP');
INSERT INTO estado (id, nome, sigla) VALUES (2, 'Rio de Janeiro', 'RJ');
INSERT INTO estado (id, nome, sigla) VALUES (3, 'Minas Gerais', 'MG');
INSERT INTO estado (id, nome, sigla) VALUES (4, 'Bahia', 'BA');
INSERT INTO estado (id, nome, sigla) VALUES (5, 'Ceará', 'CE');
INSERT INTO estado (id, nome, sigla) VALUES (6, 'Pernambuco', 'PE');
INSERT INTO estado (id, nome, sigla) VALUES (7, 'Distrito Federal', 'DF');
INSERT INTO estado (id, nome, sigla) VALUES (8, 'Paraná', 'PR');
INSERT INTO estado (id, nome, sigla) VALUES (9, 'Rio Grande do Sul', 'RS');
INSERT INTO estado (id, nome, sigla) VALUES (10, 'Amazonas', 'AM');

-- Cidades
INSERT INTO cidade (id, nome, id_estado) VALUES (1, 'São Paulo', 1);
INSERT INTO cidade (id, nome, id_estado) VALUES (2, 'Rio de Janeiro', 2);
INSERT INTO cidade (id, nome, id_estado) VALUES (3, 'Belo Horizonte', 3);
INSERT INTO cidade (id, nome, id_estado) VALUES (4, 'Salvador', 4);
INSERT INTO cidade (id, nome, id_estado) VALUES (5, 'Fortaleza', 5);
INSERT INTO cidade (id, nome, id_estado) VALUES (6, 'Recife', 6);
INSERT INTO cidade (id, nome, id_estado) VALUES (7, 'Brasília', 7);
INSERT INTO cidade (id, nome, id_estado) VALUES (8, 'Curitiba', 8);
INSERT INTO cidade (id, nome, id_estado) VALUES (9, 'Porto Alegre', 9);
INSERT INTO cidade (id, nome, id_estado) VALUES (10, 'Manaus', 10);

-- Bairros
-- São Paulo, SP
INSERT INTO bairro (id, nome, id_cidade) VALUES (1, 'Jardins', 1);
INSERT INTO bairro (id, nome, id_cidade) VALUES (2, 'Moema', 1);
INSERT INTO bairro (id, nome, id_cidade) VALUES (3, 'Pinheiros', 1);
INSERT INTO bairro (id, nome, id_cidade) VALUES (4, 'Vila Madalena', 1);
INSERT INTO bairro (id, nome, id_cidade) VALUES (5, 'Itaim Bibi', 1);

-- Rio de Janeiro, RJ
INSERT INTO bairro (id, nome, id_cidade) VALUES (6, 'Copacabana', 2);
INSERT INTO bairro (id, nome, id_cidade) VALUES (7, 'Ipanema', 2);
INSERT INTO bairro (id, nome, id_cidade) VALUES (8, 'Leblon', 2);
INSERT INTO bairro (id, nome, id_cidade) VALUES (9, 'Santa Teresa', 2);
INSERT INTO bairro (id, nome, id_cidade) VALUES (10, 'Lapa', 2);

-- Minas Gerais, MG
INSERT INTO bairro (id, nome, id_cidade) VALUES (11, 'Savassi', 3);
INSERT INTO bairro (id, nome, id_cidade) VALUES (12, 'Lourdes', 3);
INSERT INTO bairro (id, nome, id_cidade) VALUES (13, 'Santa Tereza', 3);
INSERT INTO bairro (id, nome, id_cidade) VALUES (14, 'Funcionários', 3);
INSERT INTO bairro (id, nome, id_cidade) VALUES (15, 'Gutierrez', 3);

-- Bahia, BA
INSERT INTO bairro (id, nome, id_cidade) VALUES (16, 'Barra', 4);
INSERT INTO bairro (id, nome, id_cidade) VALUES (17, 'Ondina', 4);
INSERT INTO bairro (id, nome, id_cidade) VALUES (18, 'Rio Vermelho', 4);
INSERT INTO bairro (id, nome, id_cidade) VALUES (19, 'Vitória', 4);
INSERT INTO bairro (id, nome, id_cidade) VALUES (20, 'Graça', 4);

-- Ceará, CE
INSERT INTO bairro (id, nome, id_cidade) VALUES (21, 'Meireles', 5);
INSERT INTO bairro (id, nome, id_cidade) VALUES (22, 'Aldeota', 5);
INSERT INTO bairro (id, nome, id_cidade) VALUES (23, 'Praia de Iracema', 5);
INSERT INTO bairro (id, nome, id_cidade) VALUES (24, 'Varjota', 5);
INSERT INTO bairro (id, nome, id_cidade) VALUES (25, 'Cocó', 5);

-- Pernambuco, PE
INSERT INTO bairro (id, nome, id_cidade) VALUES (26, 'Boa Viagem', 6);
INSERT INTO bairro (id, nome, id_cidade) VALUES (27, 'Recife Antigo', 6);
INSERT INTO bairro (id, nome, id_cidade) VALUES (28, 'Casa Forte', 6);
INSERT INTO bairro (id, nome, id_cidade) VALUES (29, 'Santo Antônio', 6);
INSERT INTO bairro (id, nome, id_cidade) VALUES (30, 'Pina', 6);

-- Distrito Federal, DF
INSERT INTO bairro (id, nome, id_cidade) VALUES (31, 'Asa Sul', 7);
INSERT INTO bairro (id, nome, id_cidade) VALUES (32, 'Asa Norte', 7);
INSERT INTO bairro (id, nome, id_cidade) VALUES (33, 'Lago Sul', 7);
INSERT INTO bairro (id, nome, id_cidade) VALUES (34, 'Lago Norte', 7);
INSERT INTO bairro (id, nome, id_cidade) VALUES (35, 'Sudoeste', 7);

-- Paraná, PR
INSERT INTO bairro (id, nome, id_cidade) VALUES (36, 'Batel', 8);
INSERT INTO bairro (id, nome, id_cidade) VALUES (37, 'Centro', 8);
INSERT INTO bairro (id, nome, id_cidade) VALUES (38, 'Ecoville', 8);
INSERT INTO bairro (id, nome, id_cidade) VALUES (39, 'Cabral', 8);
INSERT INTO bairro (id, nome, id_cidade) VALUES (40, 'Água Verde', 8);

-- Rio Grande do Sul, RS
INSERT INTO bairro (id, nome, id_cidade) VALUES (41, 'Moinhos de Vento', 9);
INSERT INTO bairro (id, nome, id_cidade) VALUES (42, 'Bela Vista', 9);
INSERT INTO bairro (id, nome, id_cidade) VALUES (43, 'Petrópolis', 9);
INSERT INTO bairro (id, nome, id_cidade) VALUES (44, 'Mont'Serrat', 9);
INSERT INTO bairro (id, nome, id_cidade) VALUES (45, 'Bom Fim', 9);

-- Amazonas, AM
INSERT INTO bairro (id, nome, id_cidade) VALUES (46, 'Adrianópolis', 10);
INSERT INTO bairro (id, nome, id_cidade) VALUES (47, 'Nossa Senhora das Graças', 10);
INSERT INTO bairro (id, nome, id_cidade) VALUES (48, 'Parque 10 de Novembro', 10);
INSERT INTO bairro (id, nome, id_cidade) VALUES (49, 'Cachoeirinha', 10);
INSERT INTO bairro (id, nome, id_cidade) VALUES (50, 'Aleixo', 10);'''
