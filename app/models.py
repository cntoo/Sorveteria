# app/models.py
from config import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nome):
        self.nome = nome

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome}

class Sorvete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sabor = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref=db.backref('sorvetes', lazy=True))

class SorveteNaoEncontrado(Exception):
    pass