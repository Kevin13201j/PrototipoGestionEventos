from flask import Flask, jsonify, request
from abstract_factory.event_factory import EventFactory
from Backend.abstract_factory.client_factory import ClientFactory
from DTO.event_dto import EventDTO
from DTO.client_dto import ClientDTO

app = Flask(__name__)

# Crear las fábricas
event_factory = EventFactory()
client_factory = ClientFactory()

# Crear los DAOs
event_dao_sql = event_factory.create_event_dao("sql")
event_dao_mongo = event_factory.create_event_dao("mongo")
client_dao_sql = client_factory.create_client_dao("sql")
client_dao_mongo = client_factory.create_client_dao("mongo")

# Rutas de Eventos
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json
    event = EventDTO(name=data['name'], location=data['location'], date=data['date'])
    event_dao_sql.create_event(event)
    event_dao_mongo.create_event(event)
    return jsonify({"message": "Evento agregado con éxito"}), 201

@app.route('/get_events', methods=['GET'])
def get_events():
    events_sql = event_dao_sql.get_events()
    events_mongo = event_dao_mongo.get_events()
    return jsonify({"sql_events": events_sql, "mongo_events": events_mongo})

# Rutas de Clientes
@app.route('/add_client', methods=['POST'])
def add_client():
    data = request.json
    client = ClientDTO(name=data['name'], email=data['email'], phone=data['phone'])
    client_dao_sql.create_client(client)
    client_dao_mongo.create_client(client)
    return jsonify({"message": "Cliente agregado con éxito"}), 201

@app.route('/get_clients', methods=['GET'])
def get_clients():
    clients_sql = client_dao_sql.get_clients()
    clients_mongo = client_dao_mongo.get_clients()
    return jsonify({"sql_clients": clients_sql, "mongo_clients": clients_mongo})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)