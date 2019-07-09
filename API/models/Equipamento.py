from sqlalchemy import Column, ForeignKey, Integer, String
from db import db


class EquipamentoModel(db.Model):
    __tablename__ = "equipamento"

    #Define data model to EquipamentoModel class and associates it to database table "equipamento" through SQLALchemy
    id = db.Column(String(64), primary_key=True)
    categoria = db.Column(String(64), index=True)
    data_compra = db.Column(String(64), index=True)
    data_validade = db.Column(String(64), index=True)
    data_ultima_vistoria = db.Column(String(64), index=True)

    #Define database relationship through foreign key fields
    funcionario_id = db.Column(String(64), ForeignKey('funcionario.id'))
    funcionario = db.relationship("FuncionarioModel")

    #Class initialization
    def __init__(self, id, categoria, data_compra, data_validade,
                 data_ultima_vistoria, funcionario_id):
        self.id = id
        self.categoria = categoria
        self.data_compra = data_compra
        self.data_validade = data_validade
        self.data_ultima_vistoria = data_ultima_vistoria
        self.funcionario_id = funcionario_id

    #Convert object data to JSON
    def json(self):
        return {
            'id': self.id,
            'categoria': self.categoria,
            'data_compra': self.data_compra,
            'data_validade': self.data_validade,
            'data_ultima_vistoria': self.data_ultima_vistoria,
            'funcionario_id': self.funcionario_id
        }

    # 2. Dado ID do equipamento, mostrar infos.
    # Argumentos:
    # 		codigo: ID do equipamento -> str
    # Retorna: equipamento -> EquipamentoModel
    #   tal que
    #       equipamento.id: ID do equipamento -> str
    # 		equipamento.categoria: categoria do equipamento -> str
    # 		equipamento.data_compra: formato aaaa-mm-dd -> str
    # 		equipamento.data_validade: formato aaaa-mm-dd -> str
    # 		equipamento.data_ultima_vistoria: formato aaaa-mm-dd -> str
    # 		equipamento.id_funcionario: id do funcionario a qual pertence -> int
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # 3. Dado id do funcionario, mostrar lista com [id, categoria] dos
    #    equipamentos daquele funcionario.
    # Argumentos:
    # 		id_funcionario: id do funcionario -> int
    # Retorna:
    # 		lista de dos equipamentos do funcionario -> list(EquipamentoModel)
    @classmethod
    def find_by_funcionario(cls, funcionario_id):
        return cls.query.filter_by(funcionario_id=funcionario_id).all()

    # 4. Mostrar [data de validade, id, categoria, id do funcionario] dos
    #    equipamentos ordenados a partir do mais proximo do vencimento.
    # Argumentos:
    # 		None
    # Retorna:
    # 		lista de equipamentos ordenada de forma crescente por
    #       equipamento.data_validade -> list(EquipamentoModel)
    @classmethod
    def order_by_data_validade(cls):
        return cls.query.order_by(cls.data_validade)

    #Save object data in database table
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #Delete object data from database table
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
