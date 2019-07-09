from datetime import datetime
from flask_restful import Resource, reqparse
from models.Evento import EventoModel
from models.Setor import SetorModel
from models.Funcionario import FuncionarioModel
from models.Equipamento import EquipamentoModel
from models.Sensor import SensorModel
from collections import defaultdict
import time

#Function to split arguments from string sent by Arduino
#String form: 'Sensor_id,Funcionario_id,Equipamento_1_id,...,Equipamento_N_id'
def split_arguments(ids_string):
    id_list = ids_string.split(',')
    sensor_id = id_list[0]
    funcionario_id = id_list[1]
    if len(id_list) > 2:
        equipamentos_id = id_list[2:]
    else:
        equipamentos_id = []
    return sensor_id, funcionario_id, equipamentos_id


#Given equipments list, search by category of each equipment and insert in another list
def get_equipment_list(equipamentos_id):
    equipamento_list = []
    for id in equipamentos_id:
        equipamento = EquipamentoModel.find_by_id(id.strip())
        categoria = str(equipamento.categoria).lower()
        equipamento_list.append(categoria)
    return equipamento_list


#Split equipments list
def split_equipment_list(equipamentos):
    return [e.strip().lower() for e in equipamentos.split(',')]


#Verify if some equipment is missing to some specific sector and return a string with missing equipments.
def get_missing_equipments(equipamento_list, setor_id):
    setor = SetorModel.find_by_id(setor_id)
    equipamentos_necessarios = split_equipment_list(str(setor.equipamentos))
    equipamentos_faltando = []
    for e in equipamentos_necessarios:
        if e not in equipamento_list:
            equipamentos_faltando.append(e)
    return ", ".join(equipamentos_faltando)


#Get date and time of server and return strings that contains these data.
def get_date_and_time():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    return date, time


def get_funcionario_nome(funcionario_id):
    funcionario = FuncionarioModel.find_by_id(funcionario_id)
    return funcionario.nome


#Function that receives a string from arduino and calls auxiliaries functions that
# split arguments, verify missing equipments and pass evento to post method
def create_event(ids_string):
    data, horario = get_date_and_time()
    sensor_id, funcionario_id, rfid_list = split_arguments(ids_string)
    funcionario_nome = get_funcionario_nome(funcionario_id)
    sensor = SensorModel.find_by_id(sensor_id)
    setor_id = sensor.setor_id
    equipamentos = get_equipment_list(rfid_list)
    equipamentos_faltando = get_missing_equipments(equipamentos, setor_id)
    if equipamentos_faltando:
        infracao = True
    else:
        infracao = False
    evento = EventoModel(
        id=int(round(time.time())),
        setor_id=setor_id,
        funcionario_id=funcionario_id,
        equipamentos=", ".join(equipamentos),
        data=data,
        horario=horario,
        infracao=infracao,
        equipamentos_faltando=equipamentos_faltando,
        funcionario_nome=funcionario_nome
    )
    return evento


#Resource of Evento. Validate if coming data is valid
class Evento(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('setor_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument('funcionario_id',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument('equipamentos',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument('data',
        type=str,
        required=True,
        help='Date format yyyy-mm-dd.'
    )
    parser.add_argument('horario',
        type=str,
        required=True,
        help='Time format hh:mm:ss'
    )
    parser.add_argument('infracao',
        type=bool,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument('equipamentos_faltando',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )

    #API post method
    def post(self, ids_string):
        evento = create_event(ids_string)
        try:
            evento.save_to_db()
        except:
            return {'message': "Could not save event to db."}
        return {'message': 'Event registered successfully.'}, 201


#Class related to endpoint: '/eventos_setor/<string:nome_setor>'
class EventoSetor(Resource):

    #GET method
    #Return json with API response
    def get(self, nome_setor):
        setor = SetorModel.find_by_nome(nome_setor)
        eventos = EventoModel.find_by_setor(setor.id)
        if eventos:
            return {'response': [e.json() for e in eventos]}
        return {'message': 'Nao ha eventos para este setor'}, 404


#Class related to endpoint: '/eventos_funcionario/<string:nome_funcionario> '
class EventoFuncionario(Resource):

    #GET method
    #Return json with API response
    def get(self, nome_funcionario):
        funcionario = FuncionarioModel.find_by_nome(nome_funcionario)
        eventos = EventoModel.find_by_funcionario(funcionario.id)
        if eventos:
            return {'response': [e.json() for e in eventos]}
        return {'message': 'Nao ha eventos para este funcionario'}, 404


#Class related to endpoint: '/eventos_data/<string:data>'
class EventoData(Resource):

    #GET method
    #Return json with API response
    def get(self, data):
        eventos = EventoModel.find_by_data(data)
        if eventos:
            return {'response': [e.json() for e in eventos]}
        return {'message': 'Nao ha eventos para esta data'}, 404


#Class related to endpoint: '/eventos_infracao/'
class EventoInfracao(Resource):

    #GET method
    #Return json with API response
    def get(self):
        eventos = EventoModel.find_by_infracao()
        if eventos:
            return {'response': [e.json() for e in eventos]}
        return {'message': 'Nao ha infracoes'}, 404


#Class related to endpoint: '/eventos_count/<string:data_inicial>/<string:data_final>'
class EventoCount(Resource):

    #GET method
    #Return json with API response
    def get(self, data_inicial, data_final):
        lista = {}
        eventos = EventoModel.find_by_intervalo(data_inicial, data_final)
        if eventos:
            for funcionario_id, count in eventos.items():
                funcionario = FuncionarioModel.find_by_id(funcionario_id)
                lista[funcionario.nome] = count
                # lista.append((funcionario.nome, count))  #nao sei se de fato eh count
            return {'response': lista}
        return {'message': 'Nao ha infracoes nessas datas.'}


class EventoTodos(Resource):
    def get(self):
        eventos = EventoModel.get_all_entrances()
        if eventos:
            return {'response': [v.json() for v in eventos]}
        return {'message': 'Nenhum evento encontrado'}, 404
