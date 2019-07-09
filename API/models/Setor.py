from sqlalchemy import Column, Integer, String
from db import db


class SetorModel(db.Model):
    __tablename__ = "setor"

    #Define data model to SetorModel class and associates it to database table "setor" through SQLALchemy
    id = db.Column(Integer, primary_key=True)
    nome = db.Column(String(64), index=True)
    nivel_criticidade = db.Column(String(64), index=True)
    equipamentos = db.Column(String(64), index=True)

    #Class initialization
    def __init__(self, nome, id, nivel_criticidade, equipamentos):
        self.id = id
        self.nome = nome
        self.nivel_criticidade = nivel_criticidade
        self.equipamentos = equipamentos

    #Convert object data to JSON
    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'nivel_criticidade': self.nivel_criticidade,
            'equipamentos': self.equipamentos
        }

    # 1. Dado um nome do setor, mostrar suas informacoes.
    # Argumentos:
    # 		nome: nome do setor -> str
    # Retorna: setor -> SetorModel
    #   tal que
    #       setor.id: id do setor -> int
    #       setor.nome: nome do setor -> str
    # 		setor.nivel_criticidade: nivel de criticidade do setor -> str
    # 		setor.equipamentos: equipamentos necessarios para esse setor -> str
    @classmethod
    def find_by_nome(cls, nome):
        return cls.query.filter_by(nome=nome).first()

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
