import os
from dotenv import load_dotenv
from pathlib import Path
import google.generativeai as genai



#Load private keys
env_path = Path('.') / '.env'  # Pfad zur .env-Datei (im aktuellen Verzeichnis)
load_dotenv(dotenv_path=env_path)

google_api_key= os.getenv("GOOGLE_AI_PK")


genai.configure(api_key=google_api_key)


model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Wie tauschen Developer am besten .env dateien aus?")
print(response.text)
