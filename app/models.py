from app import db

class Peca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    estoque_minimo = db.Column(db.Integer, nullable=False)
    valor_custo = db.Column(db.Float, nullable=False)
    valor_venda = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Peca {self.nome}, Estoque: {self.estoque}>'