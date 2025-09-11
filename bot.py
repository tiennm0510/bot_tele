import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 4953))

async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ghép mention các admin (Telegram không cho lấy hết member nếu >200)
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    mentions = " ".join(
        [f"@{a.user.username}" if a.user.username else a.user.full_name for a in admins]
    )

    extra = " ".join(context.args) if context.args else ""
    msg = f"📢 {mentions}\n\n{extra}" if extra else f"📢 {mentions}"
    await update.message.reply_text(msg)

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("all", all_command))
    app.run_polling()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_server()
