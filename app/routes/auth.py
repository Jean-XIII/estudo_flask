from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..extensions import db, bcrypt
from ..models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    dados = request.json

    if Usuario.query.filter_by(email=dados['email']).first():
        return jsonify({'erro': 'email já cadastrado'}), 409

    usuario = Usuario(email=dados['email'])
    usuario.set_senha(dados['senha'], bcrypt)

    db.session.add(usuario)
    db.session.commit()

    return jsonify({'mensagem': 'usuário criado'})


@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    usuario = Usuario.query.filter_by(email=dados['email']).first()

    if not usuario or not usuario.validar_senha(dados['senha'], bcrypt):
        return jsonify({'erro': 'credenciais inválidas'}), 401

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={'role': usuario.role}
    )

    return jsonify({'token': token})
