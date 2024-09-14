import discord
from discord.ext import commands
import constants
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
  instances = [{"prompt": user_prompt}]
  model = messageHandler.model
  endpointpath = constants.endpoint_path
  answer = await model.predict(
    endpoint=endpointpath,
    instances=instances
  )
  await message.channel.send(answer)


  return
  #  url = constants.gemini_token
  #  response = requests.get(url)


bot.run(constants.discord_token)
