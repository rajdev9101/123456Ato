# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
from telegram import Update, InputMediaPhoto, Message, ChatMemberUpdated
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler, filters, ContextTypes
from gtts import gTTS
from io import BytesIO
import asyncio, json, random, os, time

TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"
DELETE_DELAY = 5 * 60 * 60

REPLIES_FILE = "replies.json"
PHOTOS_FILE = "photos.json"
EMOJIS_FILE = "emojis.json"
GROUPS_FILE = "groups.json"
SETTINGS_FILE = "settings.json"

def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

replies = load_json(REPLIES_FILE, {})
photos = load_json(PHOTOS_FILE, [])
emojis = load_json(EMOJIS_FILE, {})
groups = load_json(GROUPS_FILE, [])
settings = load_json(SETTINGS_FILE, {})

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_auto_delete_enabled(chat_id): return settings.get(chat_id, {}).get("auto_delete", True)
def is_reaction_enabled(chat_id): return settings.get(chat_id, {}).get("reaction", True)
def is_autoreply_enabled(chat_id): return settings.get(chat_id, {}).get("autoreply", True)

async def simulate_typing(update, context, delay=1.0):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(delay)

def auto_delete(message, context):
    if is_auto_delete_enabled(str(message.chat_id)):
        context.job_queue.run_once(lambda ctx: ctx.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id), DELETE_DELAY)

async def send_and_auto_delete(update, context, **kwargs):
    msg = await update.message.reply_text(**kwargs)
    auto_delete(msg, context)

async def send_photo_and_auto_delete(update, context, photo):
    msg = await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    auto_delete(msg, context)

async def start(update, context):
    await simulate_typing(update, context)
    await send_and_auto_delete(update, context, text="👋 Hi kaisi ho isase Milo yah Mera Boss Hai Instagram ID De Diya https://www.instagram.com/itz_dminem_official43?igsh=MTZpNGMwOGwwMWl5dA==, powered by @raj_dev_01 🚀")
    await send_and_auto_delete(update, context, text="📸 Follow me on Instagram: https://www.instagram.com/itz_dminem_official43?igsh=MTZpNGMwOGwwMWl5dA==")
    emojis_list = ["❤️", "🔥", "😍", "😄", "🤖", "🥳", "💯", "😘", "😎", "😂"]
    await send_and_auto_delete(update, context, text=random.choice(emojis_list))
    if photos:
        await send_photo_and_auto_delete(update, context, random.choice(photos))

async def help_command(update, context):
    await simulate_typing(update, context)
    await send_and_auto_delete(update, context, text="""
🤖 *Bot Commands:*
/start - Show welcome & animation
/help - Show this help
/alive - Check if bot is alive
/ping - Show ping in ms
/font - Fancy font style
/say - Voice message
/raj - Add JPG photo (PM only)
/rajkumar - View uploaded photos
/settings - Emoji & features
/groups - Show/remove groups
/offilter - Add: hi = hello / remove hi / show hi
/autodelete on/off - Enable/disable delete
""", parse_mode="Markdown")

async def alive(update, context):
    await simulate_typing(update, context)
    await send_and_auto_delete(update, context, text="✅ I'm alive and running!")

async def ping(update, context):
    start = time.time()
    msg = await update.message.reply_text("⏱ Calculating ping...")
    latency = int((time.time() - start) * 1000)
    await msg.edit_text(f"📡 Ping: {latency} ms")
    auto_delete(msg, context)

async def font(update, context):
    if not context.args:
        await send_and_auto_delete(update, context, text="✍️ Use: /font yourtext")
        return
    text = " ".join(context.args)
    styled = f"𝗕𝗼𝗹𝗱: {text}\n𝘼𝙡𝙩: {text[::-1]}"
    await simulate_typing(update, context)
    await send_and_auto_delete(update, context, text=styled)

async def say(update, context):
    if not context.args:
        await send_and_auto_delete(update, context, text="🔊 Use: /say your message")
        return
    text = " ".join(context.args)
    tts = gTTS(text=text, lang='en')
    buf = BytesIO(); tts.write_to_fp(buf); buf.seek(0)
    msg = await update.message.reply_voice(voice=buf)
    auto_delete(msg, context)

async def raj(update, context):
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
        await send_and_auto_delete(update, context, text="📸 Use: /raj https://example.com/image.jpg")

async def rajkumar(update, context):
    if photos:
        await simulate_typing(update, context)
        media = [InputMediaPhoto(media=photo) for photo in photos[:10]]
        if len(media) == 1:
            msg = await update.message.reply_photo(photo=media[0].media)
            auto_delete(msg, context)
        else:
            msgs = await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)
            for m in msgs: auto_delete(m, context)
    else:
        await send_and_auto_delete(update, context, text="😕 No photo uploaded yet.")

async def autodelete(update, context):
    cid = str(update.effective_chat.id)
    if not context.args:
        status = "enabled" if is_auto_delete_enabled(cid) else "disabled"
        await send_and_auto_delete(update, context, text=f"🛠 Auto-delete is {status}. Use /autodelete on/off")
        return
    flag = context.args[0].lower()
    settings[cid] = settings.get(cid, {})
    settings[cid]["auto_delete"] = flag in ["on", "enable"]
    save_json(SETTINGS_FILE, settings)
    msg = "✅ Enabled." if settings[cid]["auto_delete"] else "❌ Disabled."
    await send_and_auto_delete(update, context, text=msg)

async def groups_cmd(update, context):
    cid = str(update.effective_chat.id)
    if context.args and context.args[0] == "remove":
        if cid in groups:
            groups.remove(cid)
            save_json(GROUPS_FILE, groups)
            await send_and_auto_delete(update, context, text="✅ Group removed.")
        else:
            await send_and_auto_delete(update, context, text="⚠️ Group not found.")
    else:
        msg = "\n".join(groups) if groups else "ℹ️ No groups added yet."
        await send_and_auto_delete(update, context, text=f"📋 Groups:\n{msg}")

async def offilter(update, context):
    if not context.args:
        await send_and_auto_delete(update, context, text="🧠 Use:\n/offilter hi = hello\n/offilter remove hi\n/offilter hi")
        return
    joined = " ".join(context.args)
    if joined.lower().startswith("remove"):
        try:
            _, key = joined.split("remove", 1)
            key = key.strip().lower()
            if key in replies:
                del replies[key]
                save_json(REPLIES_FILE, replies)
                await send_and_auto_delete(update, context, text=f"🗑 Removed: {key}")
            else:
                await send_and_auto_delete(update, context, text="⚠️ Keyword not found.")
        except:
            await send_and_auto_delete(update, context, text="❌ Use: /offilter remove hi")
        return
    if "=" not in joined and len(context.args) == 1:
        key = joined.strip().lower()
        if key in replies:
            await send_and_auto_delete(update, context, text=f"📥 {key} → {replies[key]}")
        else:
            await send_and_auto_delete(update, context, text="❌ Reply not found.")
        return
    try:
        key, val = joined.split("=", 1)
        key, val = key.strip().lower(), val.strip()
        replies[key] = val
        save_json(REPLIES_FILE, replies)
        await send_and_auto_delete(update, context, text=f"✅ Added: {key} → {val}")
    except:
        await send_and_auto_delete(update, context, text="❌ Format error. Use: /offilter hi = hello")

async def settings_cmd(update, context):
    cid = str(update.effective_chat.id)
    if not context.args:
        emoji = emojis.get(cid, "Not set")
        react = "on" if is_reaction_enabled(cid) else "off"
        reply = "on" if is_autoreply_enabled(cid) else "off"
        await send_and_auto_delete(update, context, text=f"Emoji: {emoji}\nReaction: {react}\nAuto-reply: {reply}\nUse /settings emoji 😍 OR /settings reaction on/off OR /settings autoreply on/off")
        return
    if context.args[0] == "emoji" and len(context.args) == 2:
        emojis[cid] = context.args[1]
        save_json(EMOJIS_FILE, emojis)
        await send_and_auto_delete(update, context, text=f"✅ Emoji set to {context.args[1]}")
    elif context.args[0] in ["reaction", "autoreply"] and len(context.args) == 2:
        key = context.args[0]
        settings[cid] = settings.get(cid, {})
        settings[cid][key] = context.args[1].lower() == "on"
        save_json(SETTINGS_FILE, settings)
        await send_and_auto_delete(update, context, text=f"✅ {key.capitalize()} set to {context.args[1].lower()}")
    else:
        await send_and_auto_delete(update, context, text="⚙️ Use: /settings emoji 😍 OR /settings reaction on/off OR /settings autoreply on/off")

async def welcome(update: ChatMemberUpdated, context):
    user = update.chat_member.new_chat_member.user
    await context.bot.send_message(chat_id=update.chat_member.chat.id, text=f"👋 Welcome {user.full_name}! Powered by @raj_dev_01 🚀")
    cid = str(update.chat_member.chat.id)
    if cid not in groups:
        groups.append(cid)
        save_json(GROUPS_FILE, groups)

# ✅ Group Added Custom Message
async def group_join_welcome(update: ChatMemberUpdated, context):
    result = update.chat_member
    if result.new_chat_member.status in ["member", "administrator", "creator"]:
        if result.old_chat_member.status == "left":
            await context.bot.send_message(
                chat_id=update.chat_member.chat.id,
                text=(
                    f"🔰 Hello everyone! aap sabhi ko dhanyvad mere ko is group mein add karne ke liye niche Mera Instagram hai agar baat karna hai to message karna👇.\n"
                    f"📸 Follow on Instagram: "
                    f"✅ Powered by 👉@raj_dev_01"
                )
            )

sent_emojis = {}
async def auto_reply(update, context):
    text = update.message.text.lower()
    cid = str(update.effective_chat.id)
    await simulate_typing(update, context, delay=0.8)
    if not is_autoreply_enabled(cid): return
    if text in replies:
        await send_and_auto_delete(update, context, text=replies[text])
    elif is_reaction_enabled(cid):
        all_emojis = ["❤️", "😂", "😍", "🔥", "😄", "😎", "🥳", "😘", "💯", "🤖"]
        used = sent_emojis.get(cid, [])
        remaining = [e for e in all_emojis if e not in used]
        emoji = random.choice(remaining or all_emojis)
        await send_and_auto_delete(update, context, text=emoji)
        if len(used) >= len(all_emojis): sent_emojis[cid] = []
        else: used.append(emoji); sent_emojis[cid] = used

# Register
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
app.add_handler(CommandHandler("autodelete", autodelete))
app.add_handler(CommandHandler("groups", groups_cmd))
app.add_handler(CommandHandler("offilter", offilter))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))
app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
app.add_handler(ChatMemberHandler(group_join_welcome, ChatMemberHandler.MY_CHAT_MEMBER))

print("🤖 Bot is running... powered by @raj_dev_01")
app.run_polling()
