# don't remove credit @raj_dev_01
from telegram import Update, InputMediaPhoto, Message
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler, filters, ContextTypes
from gtts import gTTS
from io import BytesIO
import asyncio, json, random, os, time

TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"  # Replace with your token
DELETE_DELAY = 5 * 60 * 60  # 5 hours in seconds

# File paths
REPLIES_FILE = "replies.json"
PHOTOS_FILE = "photos.json"
EMOJIS_FILE = "emojis.json"
GROUPS_FILE = "groups.json"
SETTINGS_FILE = "settings.json"

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
settings = load_json(SETTINGS_FILE, {})

# Save helpers
def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Check if auto delete is enabled for chat
def is_auto_delete_enabled(chat_id: str) -> bool:
    return settings.get(chat_id, {}).get("auto_delete", True)

def is_reaction_enabled(chat_id: str) -> bool:
    return settings.get(chat_id, {}).get("reaction", True)

# Typing simulation
async def simulate_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, delay=1.0):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(delay)

# Auto delete helper
def auto_delete(message: Message, context: ContextTypes.DEFAULT_TYPE):
    if is_auto_delete_enabled(str(message.chat_id)):
        context.job_queue.run_once(lambda ctx: ctx.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id), DELETE_DELAY)

# Wrapper to send message and auto delete
async def send_and_auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs):
    msg = await update.message.reply_text(**kwargs)
    auto_delete(msg, context)

# Wrapper to send photo and auto delete
async def send_photo_and_auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE, photo):
    msg = await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    auto_delete(msg, context)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await send_and_auto_delete(update, context, text="👋 Welcome! I'm alive and kicking, powered by @raj_dev_01 🚀")
    emoji_reactions = ["❤️", "🔥", "😍", "😄", "🤖", "🥳", "💯", "😘", "😎", "😂"]
    await send_and_auto_delete(update, context, text=random.choice(emoji_reactions))
    if photos:
        await send_photo_and_auto_delete(update, context, random.choice(photos))

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    msg = await update.message.reply_text(
        "🤖 *Bot Commands:*\n"
        "/start - Show welcome & animation\n"
        "/help - Show this help\n"
        "/alive - Check if bot is alive\n"
        "/ping - Show bot response time\n"
        "/font - Fancy font style\n"
        "/say - Speak with voice\n"
        "/raj - Upload photo (PM only, JPG)\n"
        "/rajkumar - Show uploaded photos\n"
        "/settings emoji 😍\n"
        "/settings reaction on/off\n"
        "/groups - List & remove groups\n"
        "/autodelete on/off - Enable/Disable message auto delete\n"
        "/offilter hi = hello\n\n"
        "_Just message me anything!_", parse_mode="Markdown")
    auto_delete(msg, context)

# /alive
async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await send_and_auto_delete(update, context, text="✅ I'm alive and running!")

# /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("⏱ Calculating ping...")
    end_time = time.time()
    latency = int((end_time - start_time) * 1000)
    await msg.edit_text(f"📡 Ping: {latency} ms")
    auto_delete(msg, context)

# /font
async def font(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await send_and_auto_delete(update, context, text="✍️ Use: /font yourtext")
        return
    text = " ".join(context.args)
    fancy = f"𝗕𝗼𝗹𝗱: {text}\n𝘼𝙡𝙩: {text[::-1]}"
    await simulate_typing(update, context)
    await send_and_auto_delete(update, context, text=fancy)

# /say
async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await send_and_auto_delete(update, context, text="🔊 Use: /say your message")
        return
    text = " ".join(context.args)
    tts = gTTS(text=text, lang='en')
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    msg = await update.message.reply_voice(voice=buf)
    auto_delete(msg, context)

# /raj
async def raj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        await send_and_auto_delete(update, context, text="❌ Only PM users can add photos.")
        return
    if context.args:
        url = context.args[0]
        if url.lower().endswith(".jpg"):
            photos.append(url)
            save_json(PHOTOS_FILE, photos)
            await send_and_auto_delete(update, context, text="✅ Photo added.")
        else:
            await send_and_auto_delete(update, context, text="❌ Only JPG links allowed.")
    else:
        await send_and_auto_delete(update, context, text="📸 Send photo like: /raj https://example.com/image.jpg")

# /rajkumar
async def rajkumar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if photos:
        await simulate_typing(update, context)
        for photo in photos[:10]:
            await send_photo_and_auto_delete(update, context, photo)
    else:
        await send_and_auto_delete(update, context, text="😕 No photo uploaded yet.")

# /settings
async def settings_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not context.args:
        emoji = emojis.get(chat_id, "Not set")
        react = "on" if is_reaction_enabled(chat_id) else "off"
        await send_and_auto_delete(update, context, text=f"Emoji: {emoji}\nReaction: {react}\nUse /settings emoji 😍 OR /settings reaction on")
        return
    if context.args[0] == "emoji" and len(context.args) == 2:
        emojis[chat_id] = context.args[1]
        save_json(EMOJIS_FILE, emojis)
        await send_and_auto_delete(update, context, text=f"✅ Emoji set to {context.args[1]}")
    elif context.args[0] == "reaction" and len(context.args) == 2:
        if context.args[1].lower() in ["on", "off"]:
            settings[chat_id] = settings.get(chat_id, {})
            settings[chat_id]["reaction"] = context.args[1].lower() == "on"
            save_json(SETTINGS_FILE, settings)
            await send_and_auto_delete(update, context, text=f"✅ Reaction set to {context.args[1].lower()}")
    else:
        await send_and_auto_delete(update, context, text="⚙️ Use: /settings emoji 😍 OR /settings reaction on/off")

# Add handler
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("alive", alive))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("font", font))
app.add_handler(CommandHandler("say", say))
app.add_handler(CommandHandler("raj", raj))
app.add_handler(CommandHandler("rajkumar", rajkumar))
app.add_handler(CommandHandler("settings", settings_cmd))

print("🤖 Bot is running... powered by @raj_dev_01")
app.run_polling()
