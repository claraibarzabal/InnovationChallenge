import requests

# Configura tu endpoint y clave
endpoint = 'https://<your-endpoint>/contentmoderator/moderate'
subscription_key = '<your-subscription-key>'

def check_content(content):
    """Verifica el contenido usando el servicio Content Moderator de Azure."""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }
        response = requests.post(endpoint, json={"data": content}, headers=headers)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        return response.json()  # Devuelve los resultados de la moderación
    except requests.exceptions.RequestException as error:
        print('Error checking content:', error)
        return None  # Maneja el error como consideres
