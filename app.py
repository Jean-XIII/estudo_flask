from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'chave-super-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable=False)
    senha_hash = db.Column(db.String(120), nullable = False)
    
    def set_senha(self, senha_clara):
        self.senha_hash = bcrypt.generate_password_hash(senha_clara).decode('utf-8')
    
    def validar_senha(self, senha_clara):
        return bcrypt.check_password_hash(self.senha_hash, senha_clara)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)

    servicos = db.relationship('Servico', backref = 'cliente')

@app.route('/clientes', methods = ['POST'])
def criar_clientes():
    dados = request.json
    nome = dados['nome']

    cliente = Cliente(nome=nome)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes', methods = ['GET'])
def listar_clientes():
    clientes = Cliente.query.all()

    lista_de_clientes = []
    for c in clientes:
        lista_de_clientes.append({'id': c.id, 'nome': c.nome})
    
    return jsonify(lista_de_clientes)

@app.route('/clientes/<int:id>/servicos', methods = ['GET'])
def listar_servicos_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}),404
    
    lista_servicos = []

    for servico in cliente.servicos:
        lista_servicos.append({'id': servico.id,
                          'titulo': servico.titulo,
                          'descricao': servico.descricao})
    
    return jsonify(lista_servicos)

@app.route('/clientes/<int:id>', methods = ['GET'])
def cliente_especifico(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}),404
    
    lista_servicos = []
    
    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes/<int:id>', methods = ['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)
    dados = request.json

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}),404
    
    cliente.nome = dados['nome']
    db.session.commit()

    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes/<int:id>', methods = ['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}),404
    
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'mensagem': 'cliente deletado com sucesso!'})

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.String(100), nullable = True)

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable = False)

@app.route('/servicos', methods = ['POST'])
def criar_servico():
    dados = request.json
    titulo = dados['titulo']
    descricao = dados.get('descricao')
    cliente_id = dados['cliente_id']

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404

    servico = Servico(titulo=titulo,
                      descricao=descricao,
                      cliente_id=cliente_id)
    db.session.add(servico)
    db.session.commit()

    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao,
                    'cliente_id': servico.cliente_id})

@app.route('/servicos', methods = ['GET'])
def listar_servicos():
    servicos = Servico.query.all()

    lista_de_servicos = []

    for servico in servicos:
        lista_de_servicos.append({'id': servico.id,
                                  'titulo': servico.titulo,
                                  'descricao': servico.descricao,
                                  'cliente_id': servico.cliente_id,
                                  'cliente_nome': servico.cliente.nome})
    
    return jsonify(lista_de_servicos)

@app.route('/servicos/<int:id>', methods = ['GET'])
def servico_especifico(id):
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({'erro': 'serviço não encontrado'}), 404
    
    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao})

@app.route('/servicos/<int:id>', methods = ['PUT'])
def atualizar_servico(id):
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({'erro': 'serviço não encontrado'}), 404
    
    dados = request.json
    titulo = dados['titulo']
    descricao = dados['descricao']

    servico.titulo = titulo
    servico.descricao = descricao

    db.session.commit()

    return jsonify({'mensagem': 'serviço atualizado com sucesso'})

@app.route('/servicos/<int:id>', methods = ['DELETE'])
def deletar_servico(id):
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({'erro': 'serviço não encontrado'}), 404
    
    db.session.delete(servico)
    db.session.commit()

    return jsonify({'mensagem': 'serviço removido com sucesso'})

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(200))

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    cliente = db.relationship('Cliente', backref=db.backref('endereco', uselist = False))

tecnico_servico = db.Table('tecnico_servico', db.Column('tecnico_id', db.Integer, db.ForeignKey('tecnico.id')), db.Column('servico_id', db.Integer, db.ForeignKey('servico.id')))

class Tecnico(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))

    servicos = db.relationship('Servico', secondary = tecnico_servico, backref = 'tecnicos')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
