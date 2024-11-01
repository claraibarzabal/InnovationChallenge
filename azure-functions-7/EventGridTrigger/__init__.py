import logging
import azure.functions as func
import os
from azure.cosmos import CosmosClient, PartitionKey
import uuid

# Configuración de Cosmos DB
cosmos_endpoint = os.getenv("CosmosDBEndpoint")
cosmos_key = os.getenv("CosmosDBKey")
database_name = "sustentabilidad-grupo7"
container_name = "ToDoList"

# Conexión a Cosmos DB
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
database = cosmos_client.get_database_client(database_name)

# Verificar si el contenedor existe, si no, crearlo
try:
    container = database.get_container_client(container_name)
    container.read()
except Exception:
    container = database.create_container(
        id=container_name,
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )

app = func.FunctionApp()

@app.event_grid_trigger(arg_name="azeventgrid")
def main(azeventgrid: func.EventGridEvent):
    logging.info('Python EventGrid trigger processed an event')
    try:
        req_body = azeventgrid.get_json()
        store_event(req_body)
        return func.HttpResponse("Datos almacenados en Cosmos DB", status_code=201)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

def store_event(req_body):
    if 'id' not in req_body:
        req_body['id'] = str(uuid.uuid4())
    container.upsert_item(req_body)
    logging.info("Datos almacenados en Cosmos DB")
