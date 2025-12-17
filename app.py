from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'chave-super-secreta'

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    servicos = db.relationship('Servico', backref='cliente')

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.String(200), nullable = True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable = False)
    usuario_id = db.Column(db.Integer, nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    senha_hash = db.Column(db.String(200), nullable = False)

    def set_senha(self, senha_clara):
        self.senha_hash = bcrypt.generate_password_hash(senha_clara).decode('utf-8')

    def validar_senha(self, senha_clara):
        return bcrypt.check_password_hash(self.senha_hash, senha_clara)

@app.route('/register', methods=['POST'])
def registrar_usuario():
    dados = request.json
    email = dados['email']
    senha = dados['senha']

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'erro': 'email já cadastrado'}), 409
    usuario = Usuario(email=email)
    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    return jsonify({'mensagem': 'usuário registrado com sucesso'})

@app.route('/login', methods = ['POST'])
def login():
    dados = request.json
    email = dados['email']
    senha = dados['senha']

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.validar_senha(senha):
        return jsonify({'erro': 'credenciais inválidas'}), 401
    
    token = create_access_token(identity = usuario.id)

    return jsonify({'token': token})


@app.route('/clientes', methods = ['POST'])
@jwt_required()
def criar_cliente():
    dados = request.json
    nome = dados['nome']

    cliente = Cliente(nome=nome)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes', methods = ['GET'])
def listar_clientes():
    clientes = Cliente.query.all()

    lista_clientes = []

    for cliente in clientes:
        lista_clientes.append({'id': cliente.id, 'nome': cliente.nome})
    
    return jsonify(lista_clientes)

@app.route('/clientes/<int:id>', methods = ['GET'])
def cliente_especifico(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404
    
    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes/<int:id>/servicos', methods = ['GET'])
def servicos_por_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'})
    
    lista_servicos_cliente = []
    for servico in cliente.servicos:
        lista_servicos_cliente.append({'id': servico.id,
                                       'titulo': servico.titulo,
                                       'descricao': servico.descricao})
    return jsonify({'cliente': cliente.nome, 'servicos': lista_servicos_cliente})

@app.route('/clientes/<int:id>', methods = ['PUT'])
@jwt_required()
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404
    
    dados = request.json
    nome = dados['nome']

    cliente.nome = nome
    db.session.commit()
    
    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes/<int:id>', methods = ['DELETE'])
@jwt_required()
def deletar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404
    
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'mensagem': 'cliente deletado com sucesso!'})

@app.route('/servicos', methods = ['POST'])
@jwt_required()
def criar_servico():
    usuario_id = get_jwt_identity()
    dados = request.json
    titulo = dados['titulo']
    descricao = dados.get('descricao')
    cliente_id = dados['cliente_id']

    cliente = Cliente.query.get(cliente_id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404

    servico = Servico(titulo=titulo, descricao=descricao, cliente_id=cliente_id, usuario_id=usuario_id)
    db.session.add(servico)
    db.session.commit()

    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao,
                    'cliente_id': servico.cliente_id,
                    'criado_por': servico.usuario_id})

@app.route('/servicos', methods = ['GET'])
def listar_servicos():
    servicos = Servico.query.all()

    lista_servicos = []

    for servico in servicos:
        lista_servicos.append({'id': servico.id,
                               'titulo': servico.titulo,
                               'descricao': servico.descricao,
                               'cliente_id': servico.cliente_id,
                               'cliente_nome': servico.cliente.nome})
    return jsonify(lista_servicos)

@app.route('/servicos/<int:id>', methods = ['GET'])
def servico_especifico(id):
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({'erro': 'serviço não encontrado'}), 404
    
    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao})

@app.route('/servicos/<int:id>', methods = ['PUT'])
@jwt_required()
def atualizar_servico(id):
    usuario_id = get_jwt_identity()
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({'erro': 'serviço não encontrado'}), 404
    
    if servico.usuario_id != usuario_id:
        return jsonify({'erro': 'acesso negado'}), 403
    
    dados = request.json
    titulo = dados['titulo']
    descricao = dados['descricao']

    servico.titulo = titulo
    servico.descricao = descricao
    db.session.commit()

    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao})

@app.route('/servicos/<int:id>', methods = ['DELETE'])
@jwt_required()
def deletar_servico(id):
    usuario_id = get_jwt_identity()
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({'erro': 'serviço não encontrado'}), 404
    
    if servico.usuario_id != usuario_id:
        return jsonify({'erro': 'acesso negado'})
    
    db.session.delete(servico)
    db.session.commit()

    return jsonify({'mensagem': 'serviço deletado com sucesso!'})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
