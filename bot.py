import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai
import shutil
import requests
import asyncio
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Global variable to track the latest chapter
current_latest_chapter = 0

def scrape_latest_chapter():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://tcbonepiecechapters.com/")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the chapters container
        chapter = soup.select_one('div[class="mb-3"]')

        if chapter:

            chapter_number = chapter.find("a").text.split("Chapter ")[1]
            chapter_title = chapter.find("div").text
            print(f"Chapter Number: {chapter_number} Chapter Title: {chapter_title}")
            base_url = "https://tcbonepiecechapters.com"
            href = chapter.find("a")["href"]
            full_url = base_url + href

            return int(chapter_number), chapter_title, full_url

        else:
            print("Chapters list not found")

        return 0, "", ""

    except Exception as e:
        print(f"Scraping error: {e}")
        return 0, "", ""
    finally:
        if 'driver' in locals():
            driver.quit()

async def chapter_checker():
    global current_latest_chapter
    await bot.wait_until_ready()
    
    # Get channel ID from environment variables
    channel_id = int(os.getenv("CHAPTER_CHANNEL_ID"))
    channel = bot.get_channel(channel_id)
    if not channel:
        print("Error: CHAPTER_CHANNEL_ID not set or invalid")
        return

    # Initial scrape to get current latest chapter
    loop = asyncio.get_event_loop()
    initial_chapter,title,chapter_url = await loop.run_in_executor(None, scrape_latest_chapter)
    if initial_chapter > 0:
        current_latest_chapter = initial_chapter
        
        print(f"Initial latest chapter set to: {current_latest_chapter}, with the title: {title}")
        embed = discord.Embed(
        title=f"One Piece Chapter {current_latest_chapter} is out! 🎉",
        description=f"**Title:** {new_title}",
        color=discord.Color.red(),
        url=chapter_url
        )
        # Add an image (replace URL with your actual image URL)
        embed.set_image(url="https://cdn.onepiecechapters.com/file/CDN-M-A-N/op_1009_00-Cover-redraw-fin-wm-lvl-1.png")

        # Add a footer
        embed.set_footer(text="By Meto and Tim 🌮🤝🥨")

        # Add timestamp
        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)

        await channel.send(f"<@1347316942188445706>", embed=embed)
        print(f"New chapter #{new_chapter} with titel: {new_title} detected and notified!")

    while True:
        new_chapter,new_title,chapter_url = await loop.run_in_executor(None, scrape_latest_chapter)
        if new_chapter > current_latest_chapter:
            current_latest_chapter = new_chapter

            embed = discord.Embed(
            title=f"One Piece Chapter {current_latest_chapter} is out! 🎉",
            description=f"**Title:** {new_title}",
            color=discord.Color.red(),
            url=chapter_url
            )
            # Add an image (replace URL with your actual image URL)
            embed.set_image(url="https://cdn.onepiecechapters.com/file/CDN-M-A-N/op_1009_00-Cover-redraw-fin-wm-lvl-1.png")

            # Add a footer
            embed.set_footer(text="By Meto and Tim 🌮🤝🥨")

            # Add timestamp
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)

            await channel.send(f"<@&1347316942188445706>", embed=embed)
            print(f"New chapter #{new_chapter} with tit: {new_title} detected and notified!")
            await asyncio.sleep(432000)
        elif new_chapter == 0:
            print("Scraping failed, retrying later...")
        
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    google_api_key = os.getenv("GOOGLE_AI_PK")
    genai.configure(api_key=google_api_key)
    print("Bot is ready")
    bot.loop.create_task(chapter_checker())

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user: 
        return
    if not message.content.startswith("!"):
        return

    try:
        url = message.attachments[0].url
    except IndexError:
        print("No attachments found")
    else:
        r = requests.get(url, stream=True)
        imageName = '1.jpg'
        with open(imageName, 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)
            image_file = genai.upload_file(path='./1.jpg')

    try:
        if 'image_file' in locals():
            response = model.generate_content([image_file, message.content])
        else:
            response = model.generate_content(message.content)
    except UnboundLocalError:
        response = model.generate_content(message.content)

    splitted_answer = [response.text[i:i+1950] for i in range(0, len(response.text), 1950)]
    for element in splitted_answer:
        await message.channel.send(element)

# Load environment variables and run bot
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
discord_key = os.getenv("DISCORD_TOKEN")
bot.run(discord_key)