import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path
from google.cloud import aiplatform
import google.generativeai as genai

genai.configure(api_key=os.getenv["GOOGLE_AI_PK"])

#Load private keys
env_path = Path('.') / '.env'  # Pfad zur .env-Datei (im aktuellen Verzeichnis)
load_dotenv(dotenv_path=env_path)
private_key_id = os.getenv("PRIVAT_KEY_ID")
private_key = os.getenv("PRIVATE_KEY")
project_id = os.getenv("PROJECT_ID")
client_email = os.getenv("CLIENT_EMAIL")
client_id = os.getenv("CLIENT_ID")
google_auth = os.getenv("GOOGLE_AUTH")

## Create a service account by loading private Keys
service_account = {"type": "service_account",
  "project_id": project_id,
  "private_key_id": private_key_id,
  "private_key": private_key,
  "client_email": client_email,
  "client_id": client_id,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": google_auth,
  "universe_domain": "googleapis.com"
}


model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)

"""#Connect to the Gemini api endpoint
service_account = service_account
client_options = aiplatform.gapic.EndpointServiceAsyncClientOptions(client_certs=service_account)
endpoint = aiplatform.gapic.EndpointServiceAsyncClient(client_options=client_options)

async def predict(prompt):
    instances = [{"content": prompt}]
    response = await endpoint.predict(endpoint_name="YOUR_ENDPOINT_NAME", instances=instances)
    for prediction in response.predictions:
        return prediction["content"]

if __name__ == "__main__":
    asyncio.run(predict("Was ist das Wetter heute in München?"))
    """
