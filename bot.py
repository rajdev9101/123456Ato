# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
  # don't remove credit @raj_dev_01
  # don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
from telegram import Update, InputMediaPhoto, ChatMemberUpdated
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler, filters, ContextTypes
from gtts import gTTS
from io import BytesIO
import asyncio, json, random, os, time

TOKEN = "BOT_TOKEN"
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

async def simulate_typing(update, context, delay=0.8):
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
    await send_and_auto_delete(update, context, text="👋  main abhi bhi Jinda Hun बार-बार start mat dabao, powered by @raj_dev_01 🚀")
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

random_text_replies = [
    "ok 👌", "haan ✅", "nahi ❌", "hmm 🤔", "theek hai ☑️", "acha 😊", "kya? 🤔", "kyun? 😯", "suno 🎧", "sun liya 🗣️",
    "batao 💭", "thoda ruk ⏳", "ruk ja ⛔", "wait karo ⌛", "kya kar rahe ho? 🤨", "haan bhai 😎", "haan yaar 🙌", "ab kya? 😐", "kaise ho? 🤓", "sab badhiya 😎",
    "mast 😍", "badiya 🌟", "acha laga 😊", "kya scene hai? 🌇", "dekhte hain 👀", "samajh gaya 🧐", "samajh nahi aaya 😕", "phir se bolo 🗣️", "kya bola? 🤔", "dobara bol 🔄",
    "pata nahi 🤷", "mujhe nahi pata 🤷", "mujhe samajh gaya 🤮", "mujhe laga tha 🤯", "sahi hai 👍", "sahi bola ✌️", "note kar liya 🗒️", "haan pakka 😉", "nahi yaar 😒", "ok bhai 🙌",
    "main busy hoon 📅", "baad mein ⏰", "abhi nahi ⛔", "soch raha hoon 🤔", "kaam mein hoon 💼", "ruk ruk ⏳", "abhi aaya ⏱", "chal theek 👌", "dekh liya 👀", "pata chal gaya 🕵️",
    "kar raha hoon ✍️", "kar lunga 💪", "kaam ho gaya 🚀", "chup raho 🚫", "rehne do ✋", "sun ke acha laga 😊", "kya fayda? 😑", "jaldi bol ⏭️", "maza aaya 🎉", "tum bolo 💬",
    "tumhare liye kuch bhi 🥰", "tum bahut cute ho 😘", "pyaar ho gaya 💕", "babu 😍", "baby 😘", "main tumse baat nahi karunga ❌", "mujhe time chahiye ⏳", "kar dena 📆", "kar dunga 🙏", "kar do 🙏",
    "acha ho gaya 😊", "bura lag gaya 😔", "kaafi ho gaya ✅", "itna kaafi hai 👌", "abhi kaam mein hoon 💼", "later baat karte hain 🗓️", "kal milte hain 🌌", "acha laga sun ke 😊", "haan keh diya 😎", "mujhe pasand aaya 💕",
    "tumhe kya chahiye? 😶", "tumhare bina boring hai 😔", "tum mast ho 🤩", "main thik hoon 😊", "sab thik 💪", "kuch nahi 🤷", "kya chal raha hai? 😜", "kya haal hai? 🙂", "haan thik 😊", "chal milte hain 👋",
    "dobara mat bolna 😒", "kya zarurat thi? 🤔", "bata nahi sakta 🤯", "puchh mat ⛔", "kyu poochh rahe ho? 🤔", "dil se 💕", "dil chhoo gaya 🥰", "mazaak kar raha hoon 😜", "tum samajhdar ho 🤓", "aaj mood nahi 😔",
    "mood off hai 😞", "mood on hai 😊", "bas kar yaar 🚫", "mat bol yeh 😑", "bhool gaya 😅", "yaad nahi 🤦", "kya yaad dilaya! 😍", "nahi keh sakta 🤷", "aisa nahi tha 🤨", "aisa kyun? 🤔",
    "tum kuch keh rahe the 💬", "acha bola 👍", "bahut accha 🙌", "tum alag ho 😍", "tum smart ho 🤓", "tum best ho 🏆", "tum great ho 😎", "love you 💕", "miss you 😢", "sun raha hoon 🎧",
    "sun rahi hoon 🎧", "acha feel ho raha 😊", "acha lag raha 😍", "tum awesome ho 🤩", "super ho 🌟", "badhiya ho 💪", "lagta hai busy ho 📅", "busy mat ho 🙏", "jaldi wapas aao 🚪", "milne aao 🌟",
    "milte hain jaldi ⏰", "main bhi 😊", "mujhe bhi 😊", "mujhe accha nahi laga 😔", "kya socha? 🤔", "main soch raha 🤮", "main likh raha 📜", "likh raha hoon 🗒️", "kya karna hai? 🤨", "karne do 🙅",
    "bata diya 📄", "batata hoon 📃", "bol diya 💬", "bol rahi hoon 💬", "tum sun rahe ho? 🎧", "sach mein 😉", "sach bol raha hoon 🙌", "tum sach mein mast ho 🤩", "tum pagal ho 🤭", "main pagal hoon 😜",
    "acha lagta hai tumse 🥰", "tumhari yaad aayi 😢", "tumhara message aaya 📲", "kya likha? 📃", "kya samjha? 😕", "samajh lo 🤮", "sun lo 🎧", "kya kaam hai? 💼", "kaam karke aata hoon 💪", "so raha hoon 😴",
    "sone ja raha 🛌", "jaag raha hoon ☕️", "nind aa rahi 🛌", "neend lag rahi 🛌", "khana khaya? 🍽️", "maine khaya 🍽️", "bhook lagi 😷", "thoda kha lo 🍲", "abhi khata hoon 🍽️", "kha liya 🍚",
    "kya batayein 🤔", "kya kahun 🤔", "kya bolun 🤯", "main toh shock ho gaya 😱", "pagal kar diya 🤭", "tumhare chakkar mein 😜", "acha friend ho tum 🤝", "best friend ho 🏆", "bhai ho tum 👨‍👥", "bahan ho tum 👩‍👥",
    "dost ho 👨‍👧‍👦", "true friend ho 🤝", "yaar ho 👨‍👧", "mujhe hasi aa rahi 😄", "has raha hoon 😂", "rona aa raha 😢", "ro raha hoon 😭", "ro mat 🤦", "haso 😃", "khush raho 😊",
    "sad mat ho 🤦", "tension mat lo 🤓", "mujhe tension hai 😔", "tension ho gaya 🤦", "kaam ho gaya 🚀", "kaam baaki hai 📆", "yeh kya hai? 🤔", "accha idea hai 😎", "yeh sahi hai 🌟", "naya soch rahe 🤨",
    "old idea hai 📃", "nahi jam raha 🤦", "jam gaya 🤩", "jam raha 🤮", "aaya samajh mein 🤮", "aaya dhyan mein 🕵️", "nahi aaya 😕", "abhi samjha 🤨", "abhi padha 📖", "pad raha hoon 📖",
    "tum kya padh rahe 📗", "padho 📖", "likho ✍️", "kaam karo 💼", "kaam chhodo 🤦", "phone rakho 📱", "phone uthao 📲", "phone mein ho 📲", "network gaya 📶", "abhi aaya 🚗",
    "bye 🙋", "good night 🌙", "good morning ☀️", "good evening 🌇", "namaste 🙏", "pranam 🙏", "shubh ratri 🌚", "shubh prabhat 🌞", "jai shree ram 🙏", "radhe radhe 🙏"
]



async def auto_reply(update, context):
    text = update.message.text.lower()
    cid = str(update.effective_chat.id)
    await simulate_typing(update, context, delay=5.8)
    if not is_autoreply_enabled(cid): return
    if text in replies:
        await send_and_auto_delete(update, context, text=replies[text])
    else:
        reply = random.choice(random_text_replies)
        await send_and_auto_delete(update, context, text=reply)

# Register handlers
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

print("🤖 Bot is running... powered by @raj_dev_01")
app.run_polling()

                      
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
# don't remove credit @raj_dev_01
   #Na Hai mujhe Koi force main nahin karta Kisi Ko rost Bus Sara din focus yahi Jaise dekh rahe ho mere dost karta hun main kam aur dikhata hun
#         Mera Naam bus dekhte jao abhi to maine shuru Kiya Hai    
