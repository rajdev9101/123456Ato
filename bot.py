from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import random

TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"  # <-- Replace this

# Load custom replies
with open("replies.json", "r", encoding="utf-8") as f:
    replies = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! I'm alive, powered by @raj_dev_01 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 Use /start to see welcome.\n✉️ Message me anything and I’ll reply!")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "raj" in text:
        await update.message.reply_text("Yeah, I am here. Powered by @raj_dev_01 ⚡")
        return

    if text in replies:
        await update.message.reply_text(replies[text])
    else:
        emoji = random.choice(["😄", "😉", "🔥", "💡", "🚀", "🤖"])
        await update.message.reply_text(f"{emoji}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))

if __name__ == '__main__':
    app.run_polling()
