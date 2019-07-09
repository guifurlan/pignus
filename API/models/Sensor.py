from sqlalchemy import Column, ForeignKey, Integer, String
from db import db


class SensorModel(db.Model):
    __tablename__ = "sensor"

    #Define data model to SensorModel class and associates it to database table "sensor" through SQLALchemy
    id = db.Column(Integer, primary_key=True)
    nome = db.Column(String(64), index=True)
    setor_id = db.Column(Integer, ForeignKey('setor.id'))
    setor = db.relationship("SetorModel")

    #Class initialization
    def __init__(self, id, nome, setor_id):
        self.id = id
        self.nome = nome
        self.setor_id = setor_id

    #Convert object data to JSON
    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'setor_id': self.setor_id
        }

    # Dado o nome do sensor, mostrar suas informacoes.
    # Argumentos:
    # 		nome: nome do sensor
    # Retorna: sensor -> SensorModel
    #       tal que
    #       sensor.id: id do sensor -> int
    #       sensor.nome: nome do sensor -> str
    # 		sensor.setor_id: id do setor em que ele esta -> int
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
