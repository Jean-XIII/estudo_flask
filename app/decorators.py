from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from functools import wraps

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


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if get_jwt().get('role') != role:
                return jsonify({'erro': 'acesso restrito'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
