from flask_restful import Resource, reqparse
from models.Setor import SetorModel


#Resource of Setor. Validate if coming data is valid
#Class related to endpoint: '/setor/<string:nome>'
class Setor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=int,
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument('nivel_criticidade',
        type=int,
        required=True,
        help='This field cannot be left blank.'
    )
    parser.add_argument('equipamentos',
        type=str,
        required=True,
        help='This field cannot be left blank.'
    )

    #GET method
    #Return json with API response
    def get(self, nome):
        setor = SetorModel.find_by_nome(nome)
        if setor:
            return setor.json()
        return {'message': 'Setor nao encontrado'}, 404

    #API post method
    def post(self, nome):
        if SetorModel.find_by_nome(nome):
            return {
                'message': "An item with name '{}' already exists.".format(nome)
            }, 400
        data = Setor.parser.parse_args()
        setor = SetorModel(nome, **data)
        try:
            setor.save_to_db()
        except:
            return {'message': "Error."}
        return setor.json(), 201

    #API delete method
    def delete(self, nome):
        setor = SetorModel.find_by_nome(nome)
        if setor:
            setor.delete_from_db()
        return {'message': 'Item deleted.'}

    #API put method
    def put(self, nome):
        data = Setor.parser.parse_args()
        setor = SetorModel.find_by_nome(nome)
        if setor is None:
            setor = SetorModel(nome, **data)
        else:
            setor.nivel_criticidade = data['nivel_criticidade']
            setor.equipamentos = data['equipamentos']
        setor.save_to_db()
        return setor.json()


class SetorTodos(Resource):
    def get(self):
        setores = SetorModel.get_all_entrances()
        if setores:
            return {'response': [s.json() for s in setores]}
        return {'message': 'Nenhum setor encontrado'}, 404
