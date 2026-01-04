from flask import Flask
from .config import Config
from .extensions import db, bcrypt, jwt
from .routes.auth import auth_bp
from .routes.clientes import clientes_bp
from .routes.servicos import servicos_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(servicos_bp)

    with app.app_context():
        db.create_all()

    return app
