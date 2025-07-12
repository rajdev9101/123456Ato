#don't remove credit @raj_dev_01
from telegram import Update, ChatMember, ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler
import json
import random
import asyncio

TOKEN = "7777252416:AAG_KLzRrj1sHQ6SU6FynPbgw2xXZCxZGoM"  # Replace this with your token

# Load custom replies
with open("replies.json", "r", encoding="utf-8") as f:
    replies = json.load(f)

# Helper: Simulate typing
async def simulate_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, delay=1.5):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(delay)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("👋 Welcome! I'm alive and kicking, powered by @raj_dev_01 🚀")

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("🛠 Commands:\n/start - Welcome\n/help - Help menu\n/about - Bot info\n/love - Love quote\n/joke - Random joke")

# Command: /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("🤖 I’m a smart reply bot built using Python & ChatGPT, hosted by @raj_dev_01.")

# Command: /love
async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "Pyar sirf ek baar hota hai… aur jab hota hai, toh sab kuch badal jaata hai ❤️",
        "You’re the reason behind my smile 😊",
        "Tum paas hote ho toh dil ko sukoon milta hai 💞"
    ]
    await simulate_typing(update, context)
    await update.message.reply_text(random.choice(quotes))

# Command: /joke
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "Teacher: Why are you late?\nStudent: Because of the sign!\nTeacher: What sign?\nStudent: The one that says 'School Ahead, Go Slow!' 😂",
        "Boy: I love you!\nGirl: Sorry, I have a boyfriend.\nBoy: I have a math test.\nGirl: What does that have to do with anything?\nBoy: Exactly. 💔"
    ]
    await simulate_typing(update, context)
    await update.message.reply_text(random.choice(jokes))

# Auto-reply
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    await simulate_typing(update, context)

    if "raj" in text:
        await update.message.reply_text("Yeah, I am here. Powered by @raj_dev_01 ⚡")
        return

    if text in replies:
        await update.message.reply_text(replies[text])
    else:
        # Animated emoji fallback
        animated_emojis = ["😈", "⚡", "🥰", "🥳", "😘", "❤️‍🔥", "😂", "♥️", "💋", "🥵", "🎉", "🤢"]
        await update.message.reply_text(random.choice(animated_emojis))

# Welcome new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"👋 Welcome {member.full_name}! Powered by @raj_dev_01 🚀"
        )

# Run the bot
app = ApplicationBuilder().token(TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("love", love))
app.add_handler(CommandHandler("joke", joke))

# Messages
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))

# Welcome
app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

if __name__ == '__main__':
    print("🤖 Bot is running...")
    app.run_polling()
