import os
import json
from dotenv import load_dotenv
from pathlib import Path
from google.cloud import aiplatform

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


#Connect to the Gemini api endpoint
service_account = service_account
client_options = aiplatform.gapic.EndpointServiceAsyncClientOptions(client_certs=service_account)
endpoint = aiplatform.gapic.EndpointServiceAsyncClient(client_options=client_options)


