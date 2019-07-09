# PIGNUS Back-end

Autores: Laura Politi e Guilherme Furlan

Código da API de back-end utilizada no projeto Pignus.
Pignus é uma solução mobile e IoT para o controle do uso de equipamentos de segurança em empresas. A API é responsável pela comunicação entre os sensores, aplicativos dos smartphones dos técnicos de segurança e o Banco de Dados da aplicação
API desenvolvida em python e Flask framework.
Banco de dados feito usando PostgreSQL e deploy na nuvem através da plataforma Heroku.

## Getting Started

Clone o projeto em alguma pasta de seu computador utilizando o comando:

git clone  #endereço_repositorio

### Prerequisites

É necessário ter instalado em seu computador:

- Python 3
- Flask
- SQLAlchemy
- FlaskRestful

### Installing

Para fazer download do python: https://www.python.org/downloads/

Para instalar as demais bibliotecas, rodar no terminal o comando:

pip install nome_biblioteca

Ex: pip install flask

## Running the project:

Rode o seguinte comando na pasta API do repositório do projeto:

python app.py

## Deployment

Seguem instruções para realizar o deploy no Heroku:

- Clona projeto em produção do heroku em uma pasta diferente da qual está seu código: heroku git:clone -a api-pignus
- Nesta pasta que você clonou o projeto do heroku, substitua o código pelo mais atual.
- Execute os comando na seguinte ordem:
- git add .
- git commmit
- git push heroku master


