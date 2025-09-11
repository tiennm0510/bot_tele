import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token và URL
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await context.bot.get_chat_member(update.effective_chat.id)
    mentions = " ".join(
        [f"@{a.user.username}" if a.user.username else a.user.full_name for a in admins]
    )
    extra = " ".join(context.args) if context.args else ""
    msg = f"📢 {mentions}\n\n{extra}" if extra else f"📢 {mentions}"
    await update.message.reply_text(msg)

application.add_handler(CommandHandler("all", all_command))

# Route webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Set webhook khi start
async def set_webhook():
    await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))