from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import Servico, Cliente
from ..decorators import somente_dono

servicos_bp = Blueprint('servicos', __name__)

@servicos_bp.route('/servicos', methods=['POST'])
@jwt_required()
def criar_servico():
    usuario_id = int(get_jwt_identity())
    dados = request.json

    obrigatorios = {'titulo', 'cliente_id'}
    if not dados or not obrigatorios.issubset(dados):
        return jsonify({'erro': 'dados inválidos'}), 400

    cliente = Cliente.query.get(dados['cliente_id'])

    if not cliente:
        return jsonify({'erro': 'cliente não encontrado'}), 404

    if cliente.usuario_id != usuario_id:
        return jsonify({'erro': 'cliente não pertence ao usuário'}), 403

    servico = Servico(
        titulo=dados['titulo'],
        descricao=dados.get('descricao'),
        cliente_id=cliente.id,
        usuario_id=usuario_id
    )

    db.session.add(servico)
    db.session.commit()

    return jsonify({'id': servico.id, 'titulo': servico.titulo})


@servicos_bp.route('/servicos', methods=['GET'])
@jwt_required()
def listar_servicos():
    usuario_id = int(get_jwt_identity())
    servicos = Servico.query.filter_by(usuario_id=usuario_id).all()

    return jsonify([
        {
            'id': s.id,
            'titulo': s.titulo,
            'descricao': s.descricao,
            'cliente_id': s.cliente_id,
            'cliente_nome': s.cliente.nome
        }
        for s in servicos
    ])


@servicos_bp.route('/servicos/<int:id>', methods=['GET'])
@jwt_required()
@somente_dono(Servico)
def servico_especifico(servico):
    return jsonify({
        'id': servico.id,
        'titulo': servico.titulo,
        'descricao': servico.descricao
    })


@servicos_bp.route('/servicos/<int:id>', methods=['PUT'])
@jwt_required()
@somente_dono(Servico)
def atualizar_servico(servico):
    dados = request.json

    servico.titulo = dados.get('titulo', servico.titulo)
    servico.descricao = dados.get('descricao', servico.descricao)

    db.session.commit()

    return jsonify({
        'id': servico.id,
        'titulo': servico.titulo,
        'descricao': servico.descricao
    })


@servicos_bp.route('/servicos/<int:id>', methods=['DELETE'])
@jwt_required()
@somente_dono(Servico)
def deletar_servico(servico):
    db.session.delete(servico)
    db.session.commit()

    return jsonify({'mensagem': 'serviço deletado com sucesso'})
