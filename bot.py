# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import random

# Replace with your bot token
TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"

# Load custom replies from JSON
with open("replies.json", "r", encoding="utf-8") as f:
    replies = json.load(f)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! I'm alive, powered by @raj_dev_01 🚀")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 Commands:\n/start - Welcome\n/help - Show this help\nJust message me and I’ll reply!")

# Auto-reply
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "raj" in text:
        await update.message.reply_text("Yeah, I am here. Powered by @raj_dev_01 ⚡")
        return

    if text in replies:
        await update.message.reply_text(replies[text])
    else:
        emoji = random.choice([
            "😄", "😉", "🔥", "💡", "🚀", "🤖",
            "🥰", "😘", "😈", "😂", "🎉", "💋",
            "❤️", "💖", "💔", "😎", "😜", "🤩",
            "😢", "😇", "🥵", "🥳", "❤️‍🔥", "😶‍🌫️"
        ])
        await update.message.reply_text(emoji)

# Bot setup
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

# Start bot
if __name__ == "__main__":
    print("🤖 Bot is running... powered by @raj_dev_01")
    app.run_polling()
    
