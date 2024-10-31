import json
import azure.functions as func
from azure.cosmos import CosmosClient
import uuid

# Configuración de Cosmos DB
cosmos_endpoint = "<tu_endpoint>"
cosmos_key = "<tu_key>"
database_name = "nombre_base_datos"
container_name = "nombre_contenedor"

# Conexión a Cosmos DB
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
database = cosmos_client.get_database_client(database_name)
container = database.get_container_client(container_name)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        # Genera un nuevo ID si no existe en el JSON
        if 'id' not in req_body:
            # Genera un ID único
            req_body['id'] = str(uuid.uuid4())  # O puedes usar un contador si prefieres

        # Almacena los datos en Cosmos DB
        container.upsert_item(req_body)
        
        return func.HttpResponse(
            "Datos almacenados en Cosmos DB",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )


