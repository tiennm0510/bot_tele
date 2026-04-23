import requests
import xml.etree.ElementTree as ET
import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# Nạp file .env
load_dotenv()

# Lấy config từ .env
BOT_TOKEN: str = os.environ["BOT_TOKEN"]
CHAT_ID: str = os.environ["CHAT_ID"]

def get_message():
    return (f"Task này là task đầu cũng là task cuổi hỏ :(\n")


async def main():
    bot = Bot(token=BOT_TOKEN)
    message = get_message()
    await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    asyncio.run(main())