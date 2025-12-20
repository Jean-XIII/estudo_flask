from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.String(200), nullable = True)

@app.route('/clientes', methods = ['POST'])
def criar_cliente():
    dados = request.json
    nome = dados['nome']

    cliente = Cliente(nome=nome)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({'nome': nome})

@app.route('/clientes', methods = ['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    
    lista_clientes = []

    for cliente in clientes:
        lista_clientes.append({'id': cliente.id, 'nome': cliente.nome})

    return jsonify(lista_clientes)

@app.route('/clientes/<int:id>', methods =['GET'])
def listar_cliente_especifico(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404
    
    return jsonify({'id': cliente.id, 'nome': cliente.nome})

@app.route('/clientes/<int:id>', methods = ['PUT'])
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
def deletar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404
    
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'mensagem': 'cliente deltado com sucesso!'})

@app.route('/servicos', methods = ['POST'])
def criar_servico():
    dados = request.json
    titulo = dados['titulo']
    descricao = dados['descricao']

    servico = Servico(titulo=titulo, descricao = descricao)
    db.session.add(servico)
    db.session.commit()

    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao})

@app.route('/servicos', methods = ['GET'])
def listar_servicos():
    servicos = Servico.query.all()

    lista_servicos = []

    for servico in servicos:
        lista_servicos.append({'id': servico.id,
                               'titulo': servico.titulo,
                               'descricao': servico.descricao})
    return jsonify(lista_servicos)

@app.route('/servicos/<int:id>', methods = ['GET'])
def listar_servico_especifico(id):
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
    servico.titulo = dados['titulo']
    servico.descricao = dados['descricao']
    db.session.commit()

    return jsonify({'id': servico.id,
                    'titulo': servico.titulo,
                    'descricao': servico.descricao})

@app.route('/servicos/<int:id>', methods = ['DELETE'])
def deletar_servico(id):
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({'erro': 'serviço não encontrado'}), 404
    
    db.session.delete(servico)
    db.session.commit()

    return jsonify({'mensagem': 'serviço deletado com sucesso!'})
    
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
