import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)
model = genai.GenerativeModel("gemini-1.5-flash")

#Load private keys



@bot.event
async  def on_ready():
  env_path = Path('.') / '.env'  # Pfad zur .env-Datei (im aktuellen Verzeichnis)
  load_dotenv(dotenv_path=env_path)
  google_api_key= os.getenv("GOOGLE_AI_PK")
  genai.configure(api_key=google_api_key)
  # nur zum testen am anfang
  print("bot läuft")

@bot.event
async def on_message(message: discord.Message):
  if message.author == bot.user: return
  response = model.generate_content(message.content)
  
  print(response.text)
  await message.channel.send(response.text)

env_path = Path('.') / '.env'  # Pfad zur .env-Datei (im aktuellen Verzeichnis)
load_dotenv(dotenv_path=env_path)
discord_key = os.getenv("DISCORD_TOKEN")
bot.run(discord_key)
