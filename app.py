from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'chave-super-secreta'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    usuario_id = db.Column(db.Integer, nullable= False)

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

#DECORATOR
def somente_dono(model):
    def decorator(func):
        @wraps(func)
        def wrapper(id, *args, **kwargs):
            usuario_id = int(get_jwt_identity())

            recurso = model.query.get(id)
            if not recurso:
                return jsonify({'erro': 'recurso não encontrado'}), 404
            
            if recurso.usuario_id != usuario_id:
                return jsonify({'erro': 'acesso negado'}), 403
            
            return func(recurso, *args, **kwargs)
        return wrapper
    return decorator


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
    
    token = create_access_token(identity= str(usuario.id))

    return jsonify({'token': token})


@app.route('/clientes', methods = ['POST'])
@jwt_required()
def criar_cliente():
    usuario_id = int(get_jwt_identity())

    dados = request.json
    nome = dados['nome']

    cliente = Cliente(nome=nome, usuario_id=usuario_id)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes', methods = ['GET'])
@jwt_required()
def listar_clientes():
    usuario_id = int(get_jwt_identity())
    clientes = Cliente.query.filter_by(usuario_id= usuario_id).all()

    lista_clientes = []

    for cliente in clientes:
        lista_clientes.append({'id': cliente.id, 'nome': cliente.nome})
    
    return jsonify(lista_clientes)

@app.route('/clientes/<int:id>', methods = ['GET'])
@jwt_required()
@somente_dono(Cliente)
def cliente_especifico(cliente):
    
    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes/<int:id>/servicos', methods = ['GET'])
@jwt_required()
@somente_dono(Cliente)
def servicos_por_cliente(cliente):
    lista_servicos_cliente = []
    for servico in cliente.servicos:
        lista_servicos_cliente.append({'id': servico.id,
                                       'titulo': servico.titulo,
                                       'descricao': servico.descricao})
    return jsonify({'cliente': cliente.nome, 'servicos': lista_servicos_cliente})

@app.route('/clientes/<int:id>', methods = ['PUT'])
@jwt_required()
@somente_dono(Cliente)
def atualizar_cliente(cliente):
    dados = request.json
    nome = dados['nome']

    cliente.nome = nome
    db.session.commit()
    
    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes/<int:id>', methods = ['DELETE'])
@jwt_required()
@somente_dono(Cliente)
def deletar_cliente(cliente):
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'mensagem': 'cliente deletado com sucesso!'})

@app.route('/servicos', methods = ['POST'])
@jwt_required()
def criar_servico():
    usuario_id = int(get_jwt_identity())
    dados = request.json
    titulo = dados['titulo']
    descricao = dados.get('descricao')
    cliente_id = dados['cliente_id']

    cliente = Cliente.query.get(cliente_id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404
    
    if cliente.usuario_id != usuario_id:
        return jsonify({'erro': 'cliente não pertence ao usuário'}), 403

    servico = Servico(titulo=titulo, descricao=descricao, cliente_id=cliente_id, usuario_id=usuario_id)
    db.session.add(servico)
    db.session.commit()

    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao,
                    'cliente_id': servico.cliente_id,
                    'criado_por': servico.usuario_id})

@app.route('/servicos', methods = ['GET'])
@jwt_required()
def listar_servicos():
    usuario_id=int(get_jwt_identity())
    servicos = Servico.query.filter_by(usuario_id=usuario_id).all()

    lista_servicos = []

    for servico in servicos:
        lista_servicos.append({'id': servico.id,
                               'titulo': servico.titulo,
                               'descricao': servico.descricao,
                               'cliente_id': servico.cliente_id,
                               'cliente_nome': servico.cliente.nome})
    return jsonify(lista_servicos)

@app.route('/servicos/<int:id>', methods = ['GET'])
@jwt_required()
@somente_dono(Servico)
def servico_especifico(servico):
    
    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao})

@app.route('/servicos/<int:id>', methods = ['PUT'])
@jwt_required()
@somente_dono(Servico)
def atualizar_servico(servico):
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
@somente_dono(Servico)
def deletar_servico(servico):
    db.session.delete(servico)
    db.session.commit()

    return jsonify({'mensagem': 'serviço deletado com sucesso!'})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
