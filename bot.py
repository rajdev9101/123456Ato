# don't remove credit powered by @raj_dev_0 
# don't remove credit @raj_dev_01
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import random
import time

# Replace this with your actual bot token
TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"

# Load replies from file
REPLIES_FILE = "replies.json"
with open(REPLIES_FILE, "r", encoding="utf-8") as f:
    replies = json.load(f)

def save_replies():
    with open(REPLIES_FILE, "w", encoding="utf-8") as f:
        json.dump(replies, f, ensure_ascii=False, indent=2)

# Emojis
like_emojis = ["❤️", "👍", "🔥", "😍", "💯", "🥰", "😂", "🎉", "🤩", "👏"]
animated_emojis = [
    "😄", "😉", "🔥", "💡", "🚀", "🤖", "🥰", "😘", "😈", "😂", "🎉", "💋",
    "❤️", "💖", "💔", "😎", "😜", "🤩", "😢", "😇", "🥵", "🥳", "❤️‍🔥", "😶‍🌫️"
]
emoji_index = 0
user_settings = {}
PHOTO_LINK = "https://example.com/raj.jpg"  # Replace with real .jpg URL

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! I'm alive, powered by @raj_dev_01 🚀")

# Help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💡 Commands:\n"
        "/start - Welcome message\n"
        "/help - Show help menu\n"
        "/ping - Show latency\n"
        "/alive - Bot alive check\n"
        "/font <text> - Stylish font\n"
        "/raj - Upload photo (PM only)\n"
        "/rajkumar - View photo (all)\n"
        "/rajbala - Photo + channel promo\n"
        "/settings - View emoji toggles\n"
        "/set like on/off | emoji on/off\n"
        "/addreply key = value\n"
        "/offilter key"
    )
    await update.message.reply_text(text)

# Ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    await update.message.reply_text("🏓 Pong!")
    latency = round((time.time() - start) * 1000)
    await update.message.reply_text(f"⏱ {latency} ms")

# Alive
async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Yes, I'm alive & running! Powered by @raj_dev_01")

# Fonts
def convert_font(text: str, style_index: int = 0) -> str:
    fonts = [
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "αв¢∂єƒgнιנкℓмησρqяѕтυνωχуz"),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "ค๒ς๔єŦɠђเןкl๓ภ๏קợгรՇยשฬאץչ"),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "ΔβCÐΣFGHIJKLMNΘPQRSTƱVWXΨZ".lower()),
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "🝐🝑🝒🝓🝔🝕🝖🝗🝘🝙🝚🝛🝜🝝🝞🝟🝠🝡🝢🝣🝤🝥🝦🝧🝨🝩")
    ]
    return text.lower().translate(fonts[style_index % len(fonts)])

async def font(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        input_text = " ".join(context.args)
        await update.message.reply_text(convert_font(input_text, random.randint(0, 9)))
    else:
        await update.message.reply_text("⚠️ Usage: /font <your text>")

# Photo Commands
async def raj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("⚠️ Only available in private chat.")
    else:
        await update.message.reply_photo(PHOTO_LINK, caption="📸 Here's your photo. Only PM can upload.")

async def rajkumar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(PHOTO_LINK, caption="🌟 Raj’s photo for all viewers.")

async def rajbala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📸 Here's my photo & movie channel:\n"
        "🎬 Free movies daily on [Movie Hub](https://t.me/+u4cmm3JmIrFlNzZl)\n"
        "🔥 Subscribe now and enjoy binge-watching!"
    )
    await update.message.reply_photo(PHOTO_LINK, caption=msg, parse_mode="Markdown")

# Settings Commands
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    s = user_settings.get(uid, {"like": True, "emoji": True})
    await update.message.reply_text(
        f"⚙️ *Your Settings:*\n👍 Like Emojis: {'ON' if s['like'] else 'OFF'}\n🔁 Auto Emojis: {'ON' if s['emoji'] else 'OFF'}\n\n"
        "Use /set like on/off or /set emoji on/off to change.",
        parse_mode="Markdown"
    )

async def set_setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if len(context.args) != 2:
        await update.message.reply_text("⚠️ Usage: /set <like|emoji> <on|off>")
        return
    setting, value = context.args
    if setting not in ["like", "emoji"] or value not in ["on", "off"]:
        await update.message.reply_text("❌ Invalid setting or value.")
        return
    if uid not in user_settings:
        user_settings[uid] = {"like": True, "emoji": True}
    user_settings[uid][setting] = value == "on"
    await update.message.reply_text(f"✅ {setting.capitalize()} set to {value.upper()}.")

# Add & Remove Reply
async def addreply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if "=" not in text:
        await update.message.reply_text("⚠️ Use format: /addreply key = value")
        return
    key, value = map(str.strip, text.split("=", 1))
    replies[key.lower()] = value
    save_replies()
    await update.message.reply_text(f"✅ Reply added for '{key}'")

async def offilter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /offilter <key>")
        return
    key = " ".join(context.args).lower()
    if key in replies:
        del replies[key]
        save_replies()
        await update.message.reply_text(f"❌ Removed reply for '{key}'")
    else:
        await update.message.reply_text("🔍 No such key found.")

# Auto Reply
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global emoji_index
    text = update.message.text.lower()
    uid = update.effective_user.id
    s = user_settings.get(uid, {"like": True, "emoji": True})

    if text in ["hi", "hay"]:
        await update.message.reply_text("Hello dear, how are you? 🥰")
        if s["like"]:
            await update.message.reply_text(random.choice(like_emojis))
        return

    if text in replies:
        await update.message.reply_text(replies[text])
    elif s["emoji"]:
        emoji = animated_emojis[emoji_index % len(animated_emojis)]
        emoji_index += 1
        await update.message.reply_text(emoji)

# App Init
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("alive", alive))
app.add_handler(CommandHandler("font", font))
app.add_handler(CommandHandler("raj", raj))
app.add_handler(CommandHandler("rajkumar", rajkumar))
app.add_handler(CommandHandler("rajbala", rajbala))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(CommandHandler("set", set_setting))
app.add_handler(CommandHandler("addreply", addreply))
app.add_handler(CommandHandler("offilter", offilter))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

# Run
if __name__ == "__main__":
    print("🤖 Bot is running... powered by @raj_dev_01")
    app.run_polling()
