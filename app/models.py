# app/models.py
from config import db
from app.categoria.categoria_model import Categoria

class Sorvete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sabor = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref=db.backref('sorvetes', lazy=True))

    
    def __init__(self, categoria, sabor, preco, qtd):
        self.categoria = categoria
        self.sabor = sabor
        self.preco = preco
        self.qtd = qtd

    def to_dict(self):
        return {'id': self.id, 'categoria': self.categoria, 'sabor': self.sabor, 'preco': self.preco, 'qtd': self.qtd}


class SorveteNaoEncontrado(Exception):
    pass


def sorvete_por_id(id_sorvete):
    sorvete = Sorvete.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    return sorvete.to_dict()

def listar_sorvetes():
    sorvetes = Sorvete.query.all()
    return [sorvete.to_dict() for sorvete in sorvetes]

def adicionar_sorvete(sorvete_data):
    categoria = Categoria.query.filter_by(nome=sorvete_data['categoria_nome']).first()
    if not categoria:
        raise ValueError("Categoria não encontrada")
    
    novo_sorvete = Sorvete(categoria=categoria, sabor=sorvete_data['sabor'], preco=sorvete_data['preco'], qtd=sorvete_data['qtd'])
    db.session.add(novo_sorvete)
    db.session.commit()

def atualizar_sorvete(id_sorvete, novos_dados):
    sorvete = Sorvete.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    sorvete.categoria = novos_dados['categoria']
    sorvete.sabor = novos_dados['sabor']
    sorvete.preco = novos_dados['preco']
    sorvete.qtd = novos_dados['qtd']
    db.session.commit()

def excluir_sorvete(id_sorvete):
    sorvete = Sorvete.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    db.session.delete(sorvete)
    db.session.commit()