import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

import messageHandler

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
async  def on_ready():
  # nur zum testen am anfang
  print("bot läuft")

@bot.event
async def on_message(message: discord.Message):
  user_prompt = message.content
  model = messageHandler.model
  answer = model.generate_content(user_prompt)
  await message.channel.send(answer)


env_path = Path('.') / '.env'  # Pfad zur .env-Datei (im aktuellen Verzeichnis)
load_dotenv(dotenv_path=env_path)
bot.run(os.getenv("DISCORD_TOKEN"))
