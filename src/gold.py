import requests
import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# Nạp file .env
load_dotenv()

# Lấy config từ .env
BOT_TOKEN: str = os.environ["BOT_TIENNM_TOKEN"]
CHAT_ID: str = os.environ["GROUP_BO_ICH_ID"]
SJC_URL = os.environ["SJC_URL"]

def get_location(name: str) -> str:
    match name:
        case "hanoi":
            return "Hà Nội"
        case _:
            return ""

def format_price(value: int) -> str:
    if not value:  # bắt luôn None, "", 0
        return "0"
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "0"

def get_gold_price():
    resp = requests.get(SJC_URL, timeout=10)
    resp.raise_for_status()

    data = resp.json()

    prices = []
    for item in data.get("data", []):
        tensp = item.get("tensp")
        giamua = format_price(item.get("giamua"))
        giaban = format_price(item.get("giaban"))
        prices.append(f"- {tensp}: Mua vào: {giamua} - Bán ra: {giaban}")

    if not prices:
        return "⚠️ Không có dữ liệu giá vàng."
 
    chinhanh = get_location(data.get("chinhanh", ""))
    updated = data.get("updateDate", "")

    return (f"Giá vàng tại {chinhanh} cập nhật lúc {updated}:\n" +
            "\n".join(prices))

async def main():
    bot = Bot(token=BOT_TOKEN)
    message = get_gold_price()
    await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    asyncio.run(main())
