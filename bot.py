# don't remove credit @raj_dev_01
from telegram import Update, InputMediaPhoto
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler, filters, ContextTypes
from gtts import gTTS
from io import BytesIO
import asyncio, json, random, os

TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"  # Replace with your token

# File paths
REPLIES_FILE = "replies.json"
PHOTOS_FILE = "photos.json"
EMOJIS_FILE = "emojis.json"
GROUPS_FILE = "groups.json"

# Load or create files
def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return default

replies = load_json(REPLIES_FILE, {})
photos = load_json(PHOTOS_FILE, [])
emojis = load_json(EMOJIS_FILE, {})
groups = load_json(GROUPS_FILE, [])

# Save helpers
def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Typing simulation
async def simulate_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, delay=3.0):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(delay)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("👋 Welcome! I'm alive and kicking, powered by @raj_dev_01 🚀")
    emoji_reactions = ["❤️", "🔥", "😍", "😄", "🤖", "🥳", "💯", "😘", "😎", "😂"]
    await update.message.reply_text(random.choice(emoji_reactions))
    if photos:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=random.choice(photos))

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text(
        "🤖 *Bot Commands:*\n"
        "/start - Show welcome & animation\n"
        "/help - Show this help\n"
        "/alive - Check if bot is alive\n"
        "/ping - Test bot latency\n"
        "/font - Fancy font style\n"
        "/say - Speak with voice\n"
        "/raj - Upload photo (PM only, JPG)\n"
        "/rajkumar - Show uploaded photos\n"
        "/settings - Set emoji for this group\n"
        "/groups - List & remove groups\n\n"
        "_Just message me anything!_", parse_mode="Markdown"
    )

# /alive
async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("✅ I'm alive and running!")

# /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text("🏓 Pong!")

# /font
async def font(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("✍️ Use: /font yourtext")
        return
    text = " ".join(context.args)
    fancy = f"𝗕𝗼𝗹𝗱: {text}\n𝘼𝙡𝙩: {text[::-1]}"
    await simulate_typing(update, context)
    await update.message.reply_text(fancy)

# /say
async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🔊 Use: /say your message")
        return
    text = " ".join(context.args)
    tts = gTTS(text=text, lang='en')
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    await update.message.reply_voice(voice=buf)

# /raj
async def raj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        await update.message.reply_text("❌ Only PM users can add photos.")
        return
    if context.args:
        url = context.args[0]
        if url.endswith(".jpg"):
            photos.append(url)
            save_json(PHOTOS_FILE, photos)
            await update.message.reply_text("✅ Photo added.")
        else:
            await update.message.reply_text("❌ Only JPG links allowed.")
    else:
        await update.message.reply_text("📸 Send photo like: /raj https://example.com/image.jpg")

# /rajkumar
async def rajkumar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if photos:
        await update.message.reply_photo(random.choice(photos))
    else:
        await update.message.reply_text("😕 No photo uploaded yet.")

# /groups
async def groups_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if context.args and context.args[0] == "remove":
        if chat_id in groups:
            groups.remove(chat_id)
            save_json(GROUPS_FILE, groups)
            await update.message.reply_text("✅ Group removed.")
        else:
            await update.message.reply_text("⚠️ This group not tracked.")
    else:
        if groups:
            msg = "\n".join([f"- {gid}" for gid in groups])
            await update.message.reply_text(f"📃 Tracked Groups:\n{msg}")
        else:
            await update.message.reply_text("ℹ️ No groups added yet.")

# /settings
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if len(context.args) == 1:
        emoji = context.args[0]
        emojis[chat_id] = emoji
        save_json(EMOJIS_FILE, emojis)
        await update.message.reply_text(f"✅ Emoji set to {emoji}")
    else:
        current = emojis.get(chat_id, "Not set")
        await update.message.reply_text(f"ℹ️ Current emoji: {current}\nUse: /settings 😍")

# Welcome
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"👋 Welcome {member.full_name}! Powered by @raj_dev_01 🚀"
        )
    cid = str(update.chat_member.chat.id)
    if cid not in groups:
        groups.append(cid)
        save_json(GROUPS_FILE, groups)

# Auto-reply
sent_emojis = {}
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    cid = str(update.effective_chat.id)
    await simulate_typing(update, context)

    if text in ["hi", "hey", "hello"]:
        responses = replies.get(text, ["Hi there!", "Hello!", "Hey! What's up?"])
        await update.message.reply_text(random.choice(responses))
        return

    if "raj" in text:
        await update.message.reply_text("Yeah, I am here. Powered by @raj_dev_01 ⚡")
        return

    if text in replies:
        reply = replies[text]
        if isinstance(reply, list):
            reply = random.choice(reply)
        await update.message.reply_text(reply)
    else:
        default_emojis = ["❤️", "😂", "😍", "🔥", "😄", "😎", "🥳", "😘", "💯", "🤖"]
        used = sent_emojis.get(cid, [])
        remaining = [e for e in default_emojis if e not in used]
        emoji = random.choice(remaining or default_emojis)
        await update.message.reply_text(emoji)
        if len(used) >= len(default_emojis):
            sent_emojis[cid] = []
        else:
            used.append(emoji)
            sent_emojis[cid] = used

# App setup
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("alive", alive))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("font", font))
app.add_handler(CommandHandler("say", say))
app.add_handler(CommandHandler("raj", raj))
app.add_handler(CommandHandler("rajkumar", rajkumar))
app.add_handler(CommandHandler("groups", groups_cmd))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))
app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

# Run bot
if __name__ == "__main__":
    print("🤖 Bot is running... powered by @raj_dev_01")
    app.run_polling()
