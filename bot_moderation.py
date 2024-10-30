import requests

# Configura tu endpoint y clave
endpoint = 'https://<your-endpoint>/contentmoderator/moderate'
subscription_key = '<your-subscription-key>'

async def check_content(content: str):
    try:
        response = requests.post(
            endpoint,
            json={"data": content},
            headers={
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': subscription_key,
            }
        )
        return response.json()
    except Exception as e:
        print(f"Error checking content: {e}")
        return None
