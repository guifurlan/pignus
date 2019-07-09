from flask_restful import Resource, reqparse
from models.Funcionario import FuncionarioModel


#Resource of Funcionario. Validate if coming data is valid
#Class related to endpoint: '/funcionario/<string:nome>'
class Funcionario(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=str,
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument('data_nascimento',
        type=str,
        required=True,
        help="Date format aaaa-mm-dd."
    )
    parser.add_argument('genero',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('equipe',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('cargo',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('data_contratacao',
        type=str,
        required=True,
        help="Date format yyyy-mm-dd."
    )

    #GET method
    #Return json with API response
    def get(self, nome):
        funcionario = FuncionarioModel.find_by_nome(nome)
        if funcionario:
            return funcionario.json()
        return {'message': 'Funcionario nao encontrado'}, 404

    #API post method
    def post(self, nome):
        if FuncionarioModel.find_by_nome(nome):
            return {
            'message': "An item with the name '{}' already exists".format(nome)
            }, 400
        data = Funcionario.parser.parse_args()
        funcionario = FuncionarioModel(nome, **data)
        try:
            funcionario.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500
        return funcionario.json(), 201

    #API delete method
    def delete(self, nome):
        funcionario = FuncionarioModel.find_by_nome(nome)
        if funcionario:
            funcionario.delete_from_db()
        return {'message': 'Item deleted.'}

    #API put method
    def put(self, nome):
        data = Funcionario.parser.parse_args()
        funcionario = FuncionarioModel.find_by_nome(nome)
        if funcionario is None:
            funcionario = FuncionarioModel(nome, **data)
        else:
            funcionario.equipe = data['equipe']
            funcionario.cargo = data['cargo']
        funcionario.save_to_db()
        return funcionario.json()


#Class related to endpoint: '/equipe/<string:nome_equipe>'
class FuncionarioEquipe(Resource):

    #GET method
    #Return json with API response
    def get(self, nome_equipe):
        funcionarios = FuncionarioModel.find_by_equipe(nome_equipe)
        if funcionarios:
            return {'response': [f.json() for f in funcionarios]}
        return {'message': 'Funcionario nao encontrado'}, 404


class FuncionarioTodos(Resource):

    def get(self):
        funcionarios = FuncionarioModel.get_all_entrances()
        if funcionarios:
            return {'response': [f.json() for f in funcionarios]}
        return {'message': 'Nenhum funcionario encontrado'}, 404
