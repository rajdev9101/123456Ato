# don't remove credit @raj_dev_01
from telegram import Update, ChatMember
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler
import json
import random
import asyncio

TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"  # Replace this

with open("replies.json", "r", encoding="utf-8") as f:
    replies = json.load(f)

async def simulate_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, delay=1.5):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(delay)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("👋 Welcome! I'm alive and kicking, powered by @raj_dev_01 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("🛠 Commands:\n/start - Welcome\n/help - Help\n/about - Bot info\n/love - Love lines\n/joke - Random joke")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("🤖 Made with ❤️ by @raj_dev_01")

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "Tum meri duniya ho 💖",
        "Pyar sirf ek baar hota hai... aur woh ho chuka hai 🥰",
        "Aankhon mein basa hai tu, dil mein chhupa hai tu 💘"
    ]
    await simulate_typing(update, context)
    await update.message.reply_text(random.choice(quotes))

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything! 😂",
        "Boy: I love you! Girl: I have a boyfriend. Boy: I have exams. Girl: What's the connection? Boy: Exactly! 💔"
    ]
    await simulate_typing(update, context)
    await update.message.reply_text(random.choice(jokes))

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    await simulate_typing(update, context)

    if "raj" in text:
        await update.message.reply_text("Yeah, I’m here. Powered by @raj_dev_01 ⚡")
        return

    if text in replies:
        await update.message.reply_text(replies[text])
    else:
        animated_emojis = ["😈", "⚡", "🥰", "😂", "😘", "❤️‍🔥", "💋", "🔥"]
        await update.message.reply_text(random.choice(animated_emojis))

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"👋 Welcome {member.full_name}! Powered by @raj_dev_01 🚀"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("love", love))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))
app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
