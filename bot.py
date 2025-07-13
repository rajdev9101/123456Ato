# don't remove credit powered by @raj_dev_01
# don't remove credit powered by @raj_dev_01
# don't remove credit @raj_dev_01
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler,
    filters, ContextTypes
)
import json
import random
import asyncio
import os

TOKEN = "YOUR_BOT_TOKEN"  # ← यहां अपना Bot Token डालना है
ADMIN_USERNAME = "@raj_dev_01"
PHOTO_LINK = "https://example.com/raj.jpg"  # ← यहां अपनी JPG लिंक दो

# Load replies.json
if os.path.exists("replies.json"):
    with open("replies.json", "r", encoding="utf-8") as f:
        replies = json.load(f)
else:
    replies = {}

# Load emoji settings
emoji_settings_path = "emoji_settings.json"
if os.path.exists(emoji_settings_path):
    with open(emoji_settings_path, "r") as f:
        emoji_settings = json.load(f)
else:
    emoji_settings = {}

# Load group list
group_list_path = "groups.json"
if os.path.exists(group_list_path):
    with open(group_list_path, "r") as f:
        group_list = json.load(f)
else:
    group_list = []

# Emoji → sticker ID (animated stickers)
animated_stickers = {
    "😈": "CAACAgUAAxkBAAEK4jxlxdH3zNhMkRZ3mESUDQgFz6a7RAACiQ0AAiXbcFRozU7ArhYYqDQE",
    "🔥": "CAACAgUAAxkBAAEK4kJlxdI1xzHePqAef9mU0Am1I8ay7wACGwADVp29Cm_GHeZJ2zBaDwQ",
    "🙏": "CAACAgUAAxkBAAEK4kBlxdID9O6VRHcU8VaB5ZXkCEr0nwACWAADVp29Cj8LUEMCPVxHDwQ",
    "💋": "CAACAgUAAxkBAAEK4vRlx0s6XewAAQzKNRi50oy0uIb2u9YAAlkNAAJZnb0K3nNV3nvZxa0eBA",
    "🥵": "CAACAgUAAxkBAAEK4vZlx0s7FM28mITFSRM3ErQBGjWbpAACSw4AApWfZQp7P2ZUKrTgMB4E"
}

# Typing simulation
async def simulate_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, delay=1.5):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(delay)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text(f"👋 Welcome! I'm alive, powered by {ADMIN_USERNAME} 🚀")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text(
        f"🛠 *Help Menu*\n\n"
        f"🤖 This bot replies smartly & shows emoji animations!\n"
        f"👥 Works in groups too! Just add me and chat freely\n"
        f"🔧 Commands:\n"
        f"/start - Welcome@raj_dev_01\n"
        f"/help - This help menu@raj_dev_01\n"
        f"/settings 😈 😘 🔥 - Set custom emojis powered by @raj_dev_01\n"
        f"/settings reset - Delete saved emojis@raj_dev_01\n"
        f"/groups - List all groups bot is in (admin only@raj_dev_01)\n"
        f"/raj - PM-only photo\n"
        f"/rajkumar - Public photo\n\n"
        f"💬 Keep chatting! Powered by {ADMIN_USERNAME}"
    )

# /settings command
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if context.args and context.args[0] == "reset":
        emoji_settings.pop(user_id, None)
        with open(emoji_settings_path, "w") as f:
            json.dump(emoji_settings, f)
        await update.message.reply_text("🗑️ Your emoji list was reset.")
        return

    if context.args:
        emoji_settings[user_id] = {
            "emojis": context.args,
            "last_used_index": 0
        }
        with open(emoji_settings_path, "w") as f:
            json.dump(emoji_settings, f)
        await update.message.reply_text(f"✅ Your emojis set to: {' '.join(context.args)}")
    else:
        current = emoji_settings.get(user_id, {}).get("emojis", [])
        await update.message.reply_text(f"🎭 Your emojis: {' '.join(current) if current else 'None'}")

# /groups command
async def groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME.strip("@"):
        await update.message.reply_text("🚫 Only bot admin can view groups.")
        return

    if not group_list:
        await update.message.reply_text("🤷‍♂️ No groups found.")
    else:
        names = "\n".join(f"- {name}" for name in group_list)
        await update.message.reply_text(f"📜 Bot is in these groups:\n{names}")

# /raj command (PM only)
async def raj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("⚠️ Photo only available in PM.")
        return
    await simulate_typing(update, context)
    await update.message.reply_photo(photo=PHOTO_LINK, caption="📸 Raj Photo - JPG only. Use /rajkumar to view publicly.")

# /rajkumar command
async def rajkumar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_photo(photo=PHOTO_LINK, caption="🌟 Public Raj's photo view")

# Smart Auto-reply with emoji animation
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = str(update.effective_user.id)

    if text in replies:
        await simulate_typing(update, context)
        await update.message.reply_text(replies[text])
    else:
        await simulate_typing(update, context, 1.5)
        await simulate_typing(update, context, 1)

        user_data = emoji_settings.get(user_id)
        if user_data and user_data.get("emojis"):
            index = user_data["last_used_index"]
            emojis = user_data["emojis"]
            emoji = emojis[index % len(emojis)]
            emoji_settings[user_id]["last_used_index"] = (index + 1) % len(emojis)
            with open(emoji_settings_path, "w") as f:
                json.dump(emoji_settings, f)
        else:
            emoji = random.choice(list(animated_stickers.keys()))

        sticker_id = animated_stickers.get(emoji)
        if sticker_id:
            await update.message.reply_sticker(sticker=sticker_id)
        else:
            await update.message.reply_text(emoji)

# Track groups
async def group_tracker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.chat_member.chat
    if chat.type in ["group", "supergroup"]:
        group_name = chat.title
        if group_name not in group_list:
            group_list.append(group_name)
            with open(group_list_path, "w") as f:
                json.dump(group_list, f)

# Run bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(CommandHandler("groups", groups))
app.add_handler(CommandHandler("raj", raj))
app.add_handler(CommandHandler("rajdev", rajdev))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
app.add_handler(ChatMemberHandler(group_tracker, ChatMemberHandler.CHAT_MEMBER))

if __name__ == "__main__":
    print("🤖 Bot is running... powered by @raj_dev_01")
    app.run_polling()
