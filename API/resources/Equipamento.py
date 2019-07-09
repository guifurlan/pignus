from flask_restful import Resource, reqparse
from models.Equipamento import EquipamentoModel
from models.Funcionario import FuncionarioModel


#Resource of Equipamento. Validate if coming data is valid
#Class related to endpoint: '/equipamento/<string:id>'
class Equipamento(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('categoria',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument('data_compra',
        type=str,
        required=True,
        help="Date format yyyy-mm-dd."
    )
    parser.add_argument('data_validade',
        type=str,
        required=True,
        help="Date format yyyy-mm-dd."
    )
    parser.add_argument('data_ultima_vistoria',
        type=str,
        required=True,
        help="Date format yyyy-mm-dd."
    )
    parser.add_argument('funcionario_id',
        type=int,
        required=False,
        help="Associate equipment to an employee."
    )

    #GET method
    #Return json with API response
    def get(self, id):
        equipamento = EquipamentoModel.find_by_id(id)
        if equipamento:
            return equipamento.json()
        return {'message': 'Equipamento nao encontrado'}, 404

    #API post method
    def post(self, id):
        if EquipamentoModel.find_by_id(id):
            return {
                'message': "Um equipamento com o ID '{}' ja existe.".format(id)
                }, 400
        data = Equipamento.parser.parse_args()
        equipamento = EquipamentoModel(id, **data)
        try:
            equipamento.save_to_db()
        except:
            return {
            'message': 'An error occured inserting this item to db.'}, 500
        return equipamento.json(), 201

    #API delete method
    def delete(self, id):
        equipamento = EquipamentoModel.find_by_id(id)
        if equipamento:
            equipamento.delete_from_db()
        return {'message': 'Item deleted.'}

    #API put method
    def put(self, id):
        data = Equipamento.parser.parse_args()
        equipamento = EquipamentoModel.find_by_id(id)
        if equipamento is None:
            equipamento = EquipamentoModel(id, **data)
        else:
            equipamento.data_ultima_vistoria = data['data_ultima_vistoria']
            equipamento.funcionario_id = data['funcionario_id']
        equipamento.save_to_db()
        return equipamento.json()


#Class related to endpoint: '/equipamentos_funcionario/<string:nome_funcionario>'
class EquipamentoFuncionario(Resource):

    #GET method
    #Return json with API response
    def get(self, nome_funcionario):
        funcionario = FuncionarioModel.find_by_nome(nome_funcionario)
        equipamentos = EquipamentoModel.find_by_funcionario(funcionario.id)
        if equipamentos:
            return {'response': [e.json() for e in equipamentos]}
        return {'message': 'Equipamento nao encontrado'}, 404


#Class related to endpoint: '/equipamentos_validade/'
class EquipamentoValidade(Resource):

    #GET method
    #Return json with API response
    def get(self):
        equipamentos = EquipamentoModel.order_by_data_validade()
        if equipamentos:
            return {'response': [e.json() for e in equipamentos]}
        return {'message': 'Nao ha equipamentos'}, 404
