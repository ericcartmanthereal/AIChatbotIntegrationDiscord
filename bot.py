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





@bot.event
async  def on_ready():
  env_path = Path('.') / '.env'
  load_dotenv(dotenv_path=env_path)
  google_api_key= os.getenv("GOOGLE_AI_PK")
  genai.configure(api_key=google_api_key)
  print("bot läuft")

@bot.event
async def on_message(message: discord.Message):
  if message.author == bot.user: return
  if message.content.startswith("!") == False:
    return
  response = model.generate_content(message.content)
  splitted_answer = [response.text[i:i + 1950] for i in range(0, len(response.text), 1950)]
  for element in (splitted_answer):
    await message.channel.send(element)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
discord_key = os.getenv("DISCORD_TOKEN")
bot.run(discord_key)
