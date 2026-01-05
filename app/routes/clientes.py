from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import Cliente
from ..decorators import somente_dono, role_required

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['POST'])
@jwt_required()
def criar_cliente():
    usuario_id = int(get_jwt_identity())
    dados = request.json

    if 'nome' not in dados:
        return jsonify({'erro': 'nome é obrigatório'}), 400

    cliente = Cliente(nome=dados['nome'], usuario_id=usuario_id)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({'id': cliente.id, 'nome': cliente.nome})


@clientes_bp.route('/clientes', methods=['GET'])
@jwt_required()
def listar_clientes():
    usuario_id = int(get_jwt_identity())
    clientes = Cliente.query.filter_by(usuario_id=usuario_id).all()

    return jsonify([
        {'id': c.id, 'nome': c.nome}
        for c in clientes
    ])


@clientes_bp.route('/clientes/<int:id>', methods=['GET'])
@jwt_required()
@somente_dono(Cliente)
def cliente_especifico(cliente):
    return jsonify({'id': cliente.id, 'nome': cliente.nome})


@clientes_bp.route('/clientes/<int:id>', methods=['PUT'])
@jwt_required()
@somente_dono(Cliente)
def atualizar_cliente(cliente):
    dados = request.json

    if 'nome' not in dados:
        return jsonify({'erro': 'nome é obrigatório'}), 400

    cliente.nome = dados['nome']
    db.session.commit()

    return jsonify({'id': cliente.id, 'nome': cliente.nome})


@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
@jwt_required()
@somente_dono(Cliente)
def deletar_cliente(cliente):
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'mensagem': 'cliente deletado com sucesso'})


@clientes_bp.route('/admin/clientes', methods=['GET'])
@jwt_required()
@role_required('admin')
def listar_todos_clientes():
    clientes = Cliente.query.all()
    return jsonify([
        {'id': c.id, 'nome': c.nome}
        for c in clientes
    ])
