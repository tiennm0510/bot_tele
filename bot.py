import asyncio
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))

async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await context.bot.get_chat_member(update.effective_chat.id)
    mentions = " ".join(
        [f"@{a.user.username}" if a.user.username else a.user.full_name for a in admins]
    )
    extra = " ".join(context.args) if context.args else ""
    msg = f"📢 {mentions}\n\n{extra}" if extra else f"📢 {mentions}"
    await update.message.reply_text(msg)

async def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("all", all_command))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    # keep running
    await asyncio.Event().wait()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()

async def main():
    loop = asyncio.get_event_loop()
    # chạy HTTP server trong thread executor
    loop.run_in_executor(None, run_server)
    # chạy bot
    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())
