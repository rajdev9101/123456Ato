# don't remove credit powered by @raj_dev_01
# don't remove credit powered by @raj_dev_01
# don't remove credit @raj_dev_01
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ChatMemberHandler, ContextTypes, filters
)
import json
import random
import asyncio
import os

TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"  # Replace with your bot token
ADMIN_USERNAME = "@raj_dev_01"
PHOTO_LINK = "https://example.com/raj.jpg"  # Replace with your JPG link

# Reply messages
if os.path.exists("replies.json"):
    with open("replies.json", "r", encoding="utf-8") as f:
        replies = json.load(f)
else:
    replies = {}

# Emoji user settings
emoji_settings_path = "emoji_settings.json"
if os.path.exists(emoji_settings_path):
    with open(emoji_settings_path, "r") as f:
        emoji_settings = json.load(f)
else:
    emoji_settings = {}

# Groups list
group_list_path = "groups.json"
if os.path.exists(group_list_path):
    with open(group_list_path, "r") as f:
        group_list = json.load(f)
else:
    group_list = []

# Animated sticker emoji (real sticker_id)
animated_stickers = {
    "😈": "CAACAgUAAxkBAAEK4jxlxdH3zNhMkRZ3mESUDQgFz6a7RAACiQ0AAiXbcFRozU7ArhYYqDQE",
    "🔥": "CAACAgUAAxkBAAEK4kJlxdI1xzHePqAef9mU0Am1I8ay7wACGwADVp29Cm_GHeZJ2zBaDwQ",
    "💋": "CAACAgUAAxkBAAEK4vRlx0s6XewAAQzKNRi50oy0uIb2u9YAAlkNAAJZnb0K3nNV3nvZxa0eBA",
    "🥵": "CAACAgUAAxkBAAEK4vZlx0s7FM28mITFSRM3ErQBGjWbpAACSw4AApWfZQp7P2ZUKrTgMB4E",
    "😘": "CAACAgUAAxkBAAEK4wVlx1dPKykZgP4UlDRiwbT-B-FY1AACVAADVp29Cq4DCP6F7z6ADwQ"
}

# Reaction emoji rotation
reaction_emojis = ["👍", "❤️", "🔥", "😍", "😂", "🤩", "💯", "🥰", "👏", "🎉"]
reaction_index = {}

# Typing simulation
async def simulate_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, delay=1.3):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(delay)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text(f"👋 Welcome! I'm alive, powered by {ADMIN_USERNAME} 🚀")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_text(
        f"📖 *Help Menu*\n"
        f"🧠 Auto-replies | 🤖 Animated Emoji | 🔁 Reactions\n\n"
        f"💬 Type anything and I’ll respond smartly!\n"
        f"/start - Welcome message\n"
        f"/help - This help menu\n"
        f"/settings 😈 😘 🔥 - Set your emoji pack\n"
        f"/settings reset - Remove emoji pack\n"
        f"/groups - List all groups (admin only)\n"
        f"/raj - PM-only photo\n"
        f"/rajkumar - View photo publicly\n"
        f"\nPowered by {ADMIN_USERNAME}"
    )

# /settings
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
        await update.message.reply_text(f"✅ Your emojis: {' '.join(context.args)}")
    else:
        current = emoji_settings.get(user_id, {}).get("emojis", [])
        await update.message.reply_text(f"🎭 Your emojis: {' '.join(current) if current else 'None'}")

# /groups
async def groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME.strip("@"):
        await update.message.reply_text("🚫 Only admin can access group list.")
        return
    if not group_list:
        await update.message.reply_text("🤷‍♂️ No groups found.")
    else:
        msg = "\n".join(f"- {name}" for name in group_list)
        await update.message.reply_text(f"📋 Bot is in:\n{msg}")

# /raj (PM-only)
async def raj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("⚠️ Only available in PM.")
        return
    await simulate_typing(update, context)
    await update.message.reply_photo(photo=PHOTO_LINK, caption="📸 Raj Photo. Use /rajkumar to view publicly.")

# /rajkumar
async def rajkumar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    await update.message.reply_photo(photo=PHOTO_LINK, caption="🌟 Raj's photo for all")

# Auto-reply
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = str(update.effective_user.id)

    # Step 1: Check for greetings
    greetings = ["hi", "hello", "hay", "hey"]
    if text in greetings:
        await simulate_typing(update, context, 0.7)
        await update.message.reply_text("Hey there! 👋")

        # Rotate emoji "reaction" after hi
        idx = reaction_index.get(user_id, 0)
        emoji = reaction_emojis[idx % len(reaction_emojis)]
        await update.message.reply_text(emoji)
        reaction_index[user_id] = (idx + 1) % len(reaction_emojis)
        return

    # Step 2: Match in replies.json
    if text in replies:
        await simulate_typing(update, context)
        await update.message.reply_text(replies[text])
        return

    # Step 3: Emoji fallback (animated sticker)
    await simulate_typing(update, context, 1.1)
    await simulate_typing(update, context, 0.5)

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

# App setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(CommandHandler("groups", groups))
app.add_handler(CommandHandler("raj", raj))
app.add_handler(CommandHandler("rajkumar", rajkumar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
app.add_handler(ChatMemberHandler(group_tracker, ChatMemberHandler.CHAT_MEMBER))

if __name__ == "__main__":
    print("🤖 Bot is running... Powered by @raj_dev_01")
    app.run_polling()
        
