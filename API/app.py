import os

from flask import Flask, request
from flask_restful import Api
from resources.Equipamento import Equipamento, EquipamentoFuncionario, EquipamentoValidade
from resources.Evento import EventoFuncionario, EventoInfracao, EventoSetor, EventoData, Evento, EventoCount, EventoTodos
from resources.Funcionario import Funcionario, FuncionarioEquipe, FuncionarioTodos
from resources.Setor import Setor, SetorTodos
from resources.Sensor import Sensor, SensorTodos

################################################################################
#      DATABASE CREDENTIALS AND APP FLASK CONFIG FOR RUNNING LOCALLY           #
# ##############################################################################

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'database_url_credentials'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['DEBUG']=True

api = Api(app)

################################################################################
#    DATABASE CREDENTIALS AND APP FLASK CONFIG FOR RUNNING ON HEROKU           #
################################################################################
############################### DO NOT ERASE!!! ################################
# app = Flask(__name__)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# api = Api(app)

################################################################################
#------------------------------------------------------------------------------#
################################################################################

#home app endpoint
@app.route('/')
def home():
	return "Pignus Home"

#==============================================================================#
#============================== ENDPOINT API IMPLEMENTATION ===================#
#==============================================================================#

#POST - used to receive data
#GET - used to send data back only

#GET /setor/<string:nome>
#Associates endpoint '/setor/<string:nome>' to Setor resource and add it to api.
api.add_resource(Setor, '/setor/<string:nome>')

#GET all entrances on table setor.
api.add_resource(SetorTodos, '/setor_todos')

#GET all entrances on table sensor.
api.add_resource(SensorTodos, '/sensor_todos')

#GET /equipamento/<string:id>
#Associates endpoint '/equipamento/<string:id>' to Equipamento resource and add it to api.
api.add_resource(Equipamento, '/equipamento/<string:id>')

#GET /equipamentos_funcionario/<string:nome_funcionario>
#Associates endpoint '/equipamentos_funcionario/<string:nome_funcionario>' to EquipamentoFuncionario resource and add it to api.
api.add_resource(EquipamentoFuncionario, '/equipamentos_funcionario/<string:nome_funcionario>')

#GET /equipamentos_validade/
#Associates endpoint '/equipamentos_validade' to EquipamentoValidade resource and add it to api.
api.add_resource(EquipamentoValidade, '/equipamentos_validade')

#GET /funcionario/<string:nome>
#Associates endpoint 'funcionario/<string:nome>' to Funcionario resource and add it to api.
api.add_resource(Funcionario, '/funcionario/<string:nome>')

#GET /equipe/<string:nome_equipe>
#Associates endpoint '/equipe/<string:nome_equipe>' to FuncionarioEquipe resource and add it to api.
api.add_resource(FuncionarioEquipe, '/equipe/<string:nome_equipe>')

# Gets all entrances for table funcionario
api.add_resource(FuncionarioTodos, '/funcionario_todos')

#GET all entrances on table setor.
api.add_resource(EventoTodos, '/evento_todos')

#GET /eventos_setor/<string:nome_setor>
#Associates endpoint '/eventos_setor/<string:nome_setor>' to EventoSetor resource and add it to api.
api.add_resource(EventoSetor, '/eventos_setor/<string:nome_setor>')

#GET /eventos_funcionario/<string:nome_funcionario>
#Associates endpoint '/eventos_funcionario/<string:nome_funcionario>' to EventoFuncionario resource and add it to api.
api.add_resource(EventoFuncionario, '/eventos_funcionario/<string:nome_funcionario>')

#GET /eventos_data/<string:data>
#Associates endpoint '/eventos_data/<string:data>' to EventoData resource and add it to api.
api.add_resource(EventoData, '/eventos_data/<string:data>')

#GET /eventos_infracao/
#Associates endpoint '/eventos_infracao/' to EventoInfracao resource and add it to api.
api.add_resource(EventoInfracao, '/eventos_infracao')

#GET /eventos_count/<string:data_inicial>/<string:data_final>
#Associates endpoint '/eventos_count/<string:data_inicial>/<string:data_final>' to EventoCount resource and add it to api.
api.add_resource(EventoCount, '/eventos_count/<string:data_inicial>/<string:data_final>')

#POST-only. Used to register events to the database.
#ids_string format: "<id_sensor>,<id_funcionario>,<ids_dos_equipamentos>"
api.add_resource(Evento, '/evento/<string:ids_string>')

#Register a sensor in the bank.
api.add_resource(Sensor, '/sensor/<string:id>')

#==============================================================================#
#==============================================================================#
#==============================================================================#


#App and DB initialization
#Running on port 5000

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000)
