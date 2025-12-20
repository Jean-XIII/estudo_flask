# Estudo do framework Flask para criação de APIs REST backend.

## Ferramentas utilizadas:
### Flask (framework web)
[Documentação oficial do Flask](https://flask.palletsprojects.com/en/latest/) — base de TODAS as rotas, request, response.

**Tópicos abordados**: Routing, Request / Response, Decorators, Application, Context.

### SQLAlchemy (ORM – base teórica)
[Documentação principal do ORM que fundamenta tudo](https://docs.sqlalchemy.org/en/20/)

**Tópicos relevantes**: ORM Mapping, Relationships, One-to-Many, Transactions

### Flask-SQLAlchemy (ORM)
[Extensão oficial do Flask para SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/latest/)

**Tópicos abordados**: db.Model, db.Column, relationship, ForeignKey, session.add / commit.

### Flask-JWT-Extended (JWT)
[Documentação oficial da biblioteca](https://flask-jwt-extended.readthedocs.io/en/stable/)

**Tópicos estudados**: create_access_token, @jwt_required(), get_jwt_identity, JWT workflow, Authorization headers

### Flask-Bcrypt (hash de senha)
[Biblioteca padrão para hash seguro de senhas](https://flask-bcrypt.readthedocs.io/en/latest/)
**Fundamentos**: generate_password_hash, check_password_hash

### HTTP Status Codes (semântica correta)
[Fonte oficial da IANA (Internet Assigned Numbers Authority)](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml)
