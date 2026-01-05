from .extensions import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)

    servicos = db.relationship('Servico', backref='cliente')


class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')

    def set_senha(self, senha, bcrypt):
        self.senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

    def validar_senha(self, senha, bcrypt):
        return bcrypt.check_password_hash(self.senha_hash, senha)
