from flask_restful import Resource, reqparse
from models.Sensor import SensorModel


#Resource of Sensor. Validate if coming data is valid
class Sensor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nome',
        type=str,
        required=True,
        help='This field cannot be left blank.'
    )
    parser.add_argument('setor_id',
        type=int,
        required=True,
        help='This field cannot be left blank.'
    )

    #GET method
    #Return json with API response
    def get(self, nome):
        sensor = SensorModel.find_by_nome(nome)
        if sensor:
            return sensor.json()
        return {'message': 'Sensor nao encontrado'}, 404

    #API post method
    def post(self, id):
        if SensorModel.find_by_id(id):
            return {
                'message': "An item with id '{}' already exists.".format(id)
            }, 400
        data = Sensor.parser.parse_args()
        sensor = SensorModel(id, **data)
        try:
            sensor.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500
        return sensor.json(), 201

    #API delete method
    def delete(self, nome):
        sensor = SensorModel.find_by_nome(nome)
        if sensor:
            sensor.delete_from_db()
        return {'message': 'Item deleted.'}

    #API put method
    def put(self, nome):
        data = Sensor.parser.parse_args()
        sensor = SensorModel.find_by_nome(nome)
        if sensor is None:
            sensor = SensorModel(nome, **data)
        else:
            sensor.setor_id = data['setor_id']
        sensor.save_to_db()
        return sensor.json()


class SensorTodos(Resource):
    def get(self):
        sensores = SensorModel.get_all_entrances()
        if sensores:
            return {'response': [s.json() for s in sensores]}
        return {'message': 'Nenhum sensor encontrado'}, 404
