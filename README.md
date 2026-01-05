# Estudo de Flask – API REST com Autenticação e Autorização

Projeto de estudo desenvolvido para praticar e consolidar conceitos de desenvolvimento back-end com Flask, incluindo autenticação JWT, controle de acesso, relacionamento entre entidades e organização do código em módulos.

O foco do projeto não é um produto final, mas a aplicação prática de boas práticas e fundamentos comuns em APIs REST.

---

## Objetivo do projeto

Este repositório tem como objetivo estudar e praticar:

- Criação de APIs REST com Flask
- Autenticação e autorização utilizando JWT
- Controle de acesso por usuário e por papel (admin/user)
- Relacionamento entre entidades usando SQLAlchemy
- Organização de um projeto Flask utilizando Blueprints
- Separação de responsabilidades no código

---

## Funcionalidades implementadas

- Registro e login de usuários
- Autenticação via JWT
- Autorização baseada em papéis
- CRUD de clientes
- CRUD de serviços vinculados a clientes
- Restrição de acesso para que usuários só manipulem seus próprios dados
- Endpoint administrativo restrito

---

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt
- SQLite

---

## Estrutura do projeto

estudo_flask/<br>
├── app/<br>
│ ├── init.py<br>
│ ├── config.py<br>
│ ├── extensions.py<br>
│ ├── models.py<br>
│ ├── decorators.py<br>
│ └── routes/<br>
│ ├── auth.py<br>
│ ├── clientes.py<br>
│ └── servicos.py<br>
├── run.py<br>
├── requirements.txt<br>

---

## Como executar o projeto

1. Clone o repositório:
```bash
git clone https://github.com/Jean-XIII/estudo_flask.git
cd estudo_flask
```
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. (Opcional) Defina a variável de ambiente do JWT:
```bash
export JWT_SECRET_KEY=sua_chave_secreta
```
5.Execute a aplicação:
```bash
python run.py
```
A API estará disponível em:
```bash
http://localhost:5000
```
## Fluxo básico de uso
1. Registrar usuário:
```bash
POST /register
```
2. Realizar login:
```bash
POST /login
```
O login retorna um token JWT, que deve ser enviado no header das requisições protegidas:
```bash
Authorization: Bearer <token>
```
3. Utilizar os endpoints de clientes e serviços normalmente.

## Exemplos de endpoints
* POST /clientes
* GET /clientes
* PUT /clientes/<id>
* DELETE /clientes/<id>
* POST /servicos
* GET /servicos
* PUT /servicos/<id>
* DELETE /servicos/<id>
* GET /admin/clientes (acesso restrito a usuários admin)
## Observações finais
Este projeto está sendo desenvolvido exclusivamente para fins de estudo e prática, com foco em aprendizado de conceitos de back-end e organização de aplicações Flask.
