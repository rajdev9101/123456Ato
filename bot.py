# don't remove credit powered by @raj_dev_0 
# don't remove credit @raj_dev_01
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import random
import time

# Replace this with your actual bot token
TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"

# Load custom replies from replies.json
with open("replies.json", "r", encoding="utf-8") as f:
    replies = json.load(f)

# Emoji sets
like_emojis = ["❤️", "👍", "🔥", "😍", "💯", "🥰", "😂", "🎉", "🤩", "👏"]
animated_emojis = [
    "😄", "😉", "🔥", "💡", "🚀", "🤖", "🥰", "😘", "😈",
    "😂", "🎉", "💋", "❤️", "💖", "💔", "😎", "😜", "🤩",
    "😢", "😇", "🥵", "🥳", "❤️‍🔥", "😶‍🌫️"
]
emoji_index = 0

# Your photo link (raj photo)
PHOTO_LINK = "https://example.com/raj.jpg"  # replace with your real JPG URL

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! I'm alive, powered by @raj_dev_01 🚀")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💡 Commands:\n"
        "/start - Welcome message\n"
        "/help - Show help menu\n"
        "/ping - Show latency\n"
        "/alive - Bot alive check\n"
        "/font <text> - Stylish font\n"
        "/raj - Upload photo (PM only)\n"
        "/rajkumar - View photo (all)"
    )
    await update.message.reply_text(text)

# /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    await update.message.reply_text("🏓 Pong!")
    end = time.time()
    latency = round((end - start) * 1000)
    await update.message.reply_text(f"⏱ {latency} ms")

# /alive
async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Yes, I'm alive & running! Powered by @raj_dev_01")

# /font
def convert_font(text: str) -> str:
    normal = "abcdefghijklmnopqrstuvwxyz"
    fancy = "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"
    return "".join(fancy[normal.index(c)] if c in normal else c for c in text.lower())

async def font(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        input_text = " ".join(context.args)
        await update.message.reply_text(convert_font(input_text))
    else:
        await update.message.reply_text("⚠️ Usage: /font <your text>")

# /raj (only in PM)
async def raj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("⚠️ Only available in private chat.")
        return
    await update.message.reply_photo(PHOTO_LINK, caption="📸 Here's your photo. Only PM can upload.")

# /rajkumar (public view)
async def rajkumar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(PHOTO_LINK, caption="🌟 Raj’s photo for all viewers.")

# Auto-reply handler
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global emoji_index
    user_text = update.message.text.lower()

    if user_text in ["hi", "hay"]:
        await update.message.reply_text("Hello dear, how are you? 🥰")
        await update.message.reply_text(random.choice(like_emojis))
        return

    if user_text in replies:
        await update.message.reply_text(replies[user_text])
    else:
        emoji = animated_emojis[emoji_index % len(animated_emojis)]
        emoji_index += 1
        await update.message.reply_text(emoji)

# App setup
app = ApplicationBuilder().token(TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("alive", alive))
app.add_handler(CommandHandler("font", font))
app.add_handler(CommandHandler("raj", raj))
app.add_handler(CommandHandler("rajkumar", rajkumar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

# Run the bot
if __name__ == "__main__":
    print("🤖 Bot is running... powered by @raj_dev_01")
    app.run_polling()
    
