import logging
import azure.functions as func
from azure.cosmos import CosmosClient, PartitionKey
import uuid

# Configuración de Cosmos DB
cosmos_endpoint = "https://cosmosdb-7.documents.azure.com:443/"
cosmos_key = "secret_key"
database_name = "sustentabilidad-grupo7"  # Nombre de la base de datos
container_name = "ToDoList"  # Nombre del contenedor

# Conexión a Cosmos DB
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
database = cosmos_client.get_database_client(database_name)

# Verificar si el contenedor existe, si no, crearlo
try:
    container = database.get_container_client(container_name)
    container.read()  # Esto verificará si el contenedor existe
except Exception:
    container = database.create_container(
        id=container_name,
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400  # Ajusta según tus necesidades
    )

app = func.FunctionApp()

@app.event_grid_trigger(arg_name="azeventgrid")
def EventGridTrigger(azeventgrid: func.EventGridEvent):
    logging.info('Python EventGrid trigger processed an event')

    try:
        # Obtiene el cuerpo del evento, que contiene los datos
        req_body = azeventgrid.get_json()

        # Genera un nuevo ID si no existe en el JSON
        if 'id' not in req_body:
            req_body['id'] = str(uuid.uuid4())

        # Almacena los datos en Cosmos DB
        container.upsert_item(req_body)

        logging.info("Datos almacenados en Cosmos DB")
        return func.HttpResponse("Datos almacenados en Cosmos DB", status_code=201)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
