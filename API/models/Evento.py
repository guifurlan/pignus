from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import func
from db import db
from collections import defaultdict


class EventoModel(db.Model):
    __tablename__ = "evento"

    #Define data model to EventoModel class and associates it to database table "evento" through SQLALchemy
    setor_id = db.Column(Integer, ForeignKey('setor.id'))
    funcionario_id = db.Column(String(64), ForeignKey('funcionario.id'))
    equipamentos = db.Column(String(64), index=True)
    data = db.Column(String(64), index=True)
    horario = db.Column(String(64), index=True)
    infracao = db.Column(Boolean, index=True)
    equipamentos_faltando = db.Column(String(64), index=True)
    id = db.Column(Integer, primary_key=True)
    funcionario_nome = db.Column(String(64), index=True)

    #Define database relationship through foreign key fields
    setor = db.relationship("SetorModel")
    funcionario = db.relationship("FuncionarioModel")

    #Class initialization
    def __init__(self, id, setor_id, funcionario_id, equipamentos, data,
                 horario, infracao, equipamentos_faltando, funcionario_nome):
        self.id = id
        self.setor_id = setor_id
        self.funcionario_id = funcionario_id
        self.equipamentos = equipamentos
        self.data = data
        self.horario = horario
        self.infracao = infracao
        self.equipamentos_faltando = equipamentos_faltando
        self.funcionario_nome = funcionario_nome

    #Convert object data to JSON
    def json(self):
        return {
            'id': self.id,
            'setor_id': self.setor_id,
            'funcionario_id': self.funcionario_id,
            'equipamentos': self.equipamentos,
            'data': self.data,
            'horario': self.horario,
            'infracao': self.infracao,
            'equipamentos_faltando': self.equipamentos_faltando,
            'funcionario_nome': self.funcionario_nome
        }

    # 7. Dado id do setor, mostrar eventos daquele setor.
    # Argumentos:
    # 		setor_id: id do setor -> int
    # Retorna:
    # 	    Lista dos eventos daquele setor. -> list(EventoModel)
    @classmethod
    def find_by_setor(cls, setor_id):
        return cls.query.filter_by(setor_id=setor_id).all()

    # 8. Dado id do funcionario, mostrar lista de eventos envolvendo
    #    o funcionario.
    # Argumentos:
    # 		funcionario_id: id do funcionario -> int
    # Retorna:
    #       Lista dos eventos envolvendo o funcionario. -> list(EventoModel)
    @classmethod
    def find_by_funcionario(cls, funcionario_id):
        return cls.query.filter_by(funcionario_id=funcionario_id).all()

    # 9. Dada uma data, mostrar lista de eventos dessa data.
    # Argumentos:
    # 		data: data do evento, formato aaaa-mm-dd -> str
    # Retorna:
    #       Lista de eventos na data determinada. -> list(EventoModel)
    @classmethod
    def find_by_data(cls, data):
        return cls.query.filter_by(data=data).all()

    # 10. Mostrar eventos que foram infracao.
    # Argumentos:
    #       None
    # Retorna:
    #       Lista dos eventos classificados como infracao. -> list(EventoModel)
    @classmethod
    def find_by_infracao(cls):
        return cls.query.filter_by(infracao='True').all()

    # 11. Dado intervalo de datas, mostrar numero de infracoes de cada
    #     funcionario.
    # Argumentos:
    # 		data_inicial: inicio do intervalo, formato aaaa-mm-dd -> str
    # 		data_final: final do intervalo, formato aaaa-mm-dd -> str
    # Retorna:
    # 	Dicionario de ids dos funcionarios com os respectivos numeros de
    #   infracoes.
    # 		funcionario: id do funcionario -> int
    # 		infracoes: numero de infracoes -> int
    @classmethod
    def find_by_intervalo(cls, data_inicial, data_final):
        infracoes = cls.query.filter_by(infracao='True').all()
        mapeamento = defaultdict(int)
        for i in infracoes:
            if i.data >= data_inicial and i.data <= data_final:
                mapeamento[i.funcionario_id] += 1
        return mapeamento

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
