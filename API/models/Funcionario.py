from datetime import datetime
from sqlalchemy import Column, Integer, String
from db import db


class FuncionarioModel(db.Model):
    __tablename__ = "funcionario"

    #Define data model to Funcionario class and associates it to database table "funcionario" through SQLALchemy
    id = db.Column(String(64), primary_key=True)
    nome = db.Column(String(64), index=True)
    data_nascimento = db.Column(String(64), index=True)
    equipe = db.Column(String(64), index=True)
    cargo = db.Column(String(64), index=True)
    data_contratacao = db.Column(String(64), index=True)
    genero = db.Column(String(64), index=True)

    #Class initialization
    def __init__(self, nome, id, data_nascimento, equipe,
                 cargo, data_contratacao, genero):
         self.id = id
         self.nome = nome
         self.data_nascimento = data_nascimento
         self.equipe = equipe
         self.cargo = cargo
         self.data_contratacao = data_contratacao
         self.genero = genero

    #Convert object data to JSON
    def json(self):
         return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "equipe": self.equipe,
            "cargo": self.cargo,
            "data_contratacao": self.data_contratacao,
            "genero": self.genero,
         }

    # 5. Dado o nome do funcionario, mostrar suas informacoes.
    # Argumentos:
    # 		nome: nome do funcionario
    # Retorna: funcionario -> FuncionarioModel
    #   tal que
    #       funcionario.id: id do funcionario -> int
    #       funcionario.nome: nome do funcionario -> str
    # 		funcionario.data_nascimento: formato aaaa-mm-dd -> str
    # 		funcionario.equipe: nome da equipe -> str
    # 		funcionario.cargo: cargo do funcionario -> str
    # 		funcionario.data_contratacao: formato aaaa-mm-dd -> str
    # 		funcionario.genero: "M" ou "F" -> str
    @classmethod
    def find_by_nome(cls, nome):
        return cls.query.filter_by(nome=nome).first()

    # 6. Dada uma equipe, mostrar todos funcionarios dessa equipe.
    # Argumentos:
    # 		nome: nome da equipe -> str
    # Retorna:
    # 		Lista de funcionarios daquela equipe. -> list(FuncionarioModel)
    @classmethod
    def find_by_equipe(cls, equipe):
        return cls.query.filter_by(equipe=equipe).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_entrances(cls):
        return cls.query.all()

    #Save object data in database table
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #Delete object data from database table
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
