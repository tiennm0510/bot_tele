from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    members = []

    # Lấy danh sách admin (nhóm nhỏ thì có thể đổi thành get_chat_members)
    async for admin in context.bot.get_chat_administrators(chat.id):
        if admin.user.username:
            members.append(f"@{admin.user.username}")
        else:
            members.append(admin.user.full_name)

    # Ghép nội dung mà user gõ thêm phía sau /all
    extra_message = " ".join(context.args) if context.args else ""

    mentions = " ".join(members)
    text = f"📢 {mentions}\n\n{extra_message}" if extra_message else f"📢 {mentions}"

    await update.message.reply_text(text)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("all", all_command))
    app.run_polling()
