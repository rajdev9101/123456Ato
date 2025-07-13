# don't remove credit powered by @raj_dev_01
# don't remove credit powered by @raj_dev_01
from telegram import Update, ChatMember, InputMediaPhoto
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler,
    filters, ContextTypes
)
import json
import random
import asyncio
import os

TOKEN = "7793783847:AAGzbCWu1WF94yzf2_HYNbljISuFLvy5XG0"
ADMIN_USERNAME = "@raj_dev_01"
PHOTO_LINK = "https://envs.sh/eVP.jpg"  # Replace with your JPG link

# Load replies
with open("replies.json", "r", encoding="utf-8") as f:
    replies = json.load(f)

# Load or initialize emoji settings
emoji_settings = {}
if os.path.exists("emoji_settings.json"):
    with open("emoji_settings.json", "r") as f:
        emoji_settings = json.load(f)

# Load or initialize group list
group_list = []
if os.path.exists("groups.json"):
    with open("groups.json", "r") as f:
        group_list = json.load(f)

# Typing effect
async def simulate_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, delay=1.5):
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
        f"🛠 *Help Menu*\n\n"
        f"🤖 This bot replies smartly & shows emotion\n"
        f"👥 Works in groups too! Just add me and chat freely\n"
        f"🔧 Commands:\n"
        f"/start - Welcome msg\n"
        f"/help - This help menu\n"
        f"/settings [emoji] - Set your own emoji\n"
        f"/groups - Show all groups bot is in\n"
        f"/raj - PM-only photo upload info\n"
        f"/rajkumar - View raj photo (public)\n\n"
        f"🔗 Powered by {ADMIN_USERNAME}\n"
        f"💬 Keep chatting!"
    )

# /settings [emoji]
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context)
    user = str(update.effective_user.id)
    if context.args:
        emoji = context.args[0]
        emoji_settings[user] = emoji
        with open("emoji_settings.json", "w") as f:
            json.dump(emoji_settings, f)
        await update.message.reply_text(f"✅ Your emoji set to: {emoji}")
    else:
        emoji = emoji_settings.get(user, "🙂")
        await update.message.reply_text(f"🔧 Your current emoji: {emoji}\nTo change: /settings 😎")

# /groups - Show and manage groups
async def groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME.strip("@"):
        await update.message.reply_text("🚫 Only bot admin can view all groups.")
        return

    await simulate_typing(update, context)
    if not group_list:
        await update.message.reply_text("🤷‍♂️ No groups found.")
    else:
        group_names = "\n".join(f"- {g}" for g in group_list)
        await update.message.reply_text(f"📜 Groups I'm in:\n{group_names}")

# /raj - Send photo only to PM
async def raj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("⚠️ Photo upload allowed only in private chat (PM).")
        return

    await simulate_typing(update, context, delay=1)
    await simulate_typing(update, context, delay=1.5)

    await update.message.reply_photo(
        photo=PHOTO_LINK,
        caption="📸 Here's the photo.\n📂 Upload new photo via JPG link only.\n📎 Use /rajkumar to view anytime."
    )

# /rajkumar - View-only
async def rajkumar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simulate_typing(update, context, delay=1.2)
    await update.message.reply_photo(
        photo=PHOTO_LINK,
        caption="🌟 Raj's photo (view-only)"
    )

# Auto reply
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = str(update.effective_user.id)
    user_emoji = emoji_settings.get(user, None)

    if text in replies:
        await simulate_typing(update, context)
        await update.message.reply_text(replies[text])
    else:
        # Double-tap animation
        await simulate_typing(update, context, delay=1.5)
        await simulate_typing(update, context, delay=1.5)

        emoji = user_emoji or random.choice([
            "😄", "😉", "🔥", "💡", "🚀", "🤖",
            "🥰", "😘", "😈", "😂", "🎉", "💋",
            "❤️", "💖", "💔", "😎", "😜", "🤩",
            "😢", "😇", "🥵", "🥳", "❤️‍🔥", "😶‍🌫️"
        ])
        await update.message.reply_text(emoji)

# Track new group joins
async def group_tracker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = update.chat_member
    if status.new_chat_member.status == "member":
        group_name = status.chat.title
        if group_name not in group_list:
            group_list.append(group_name)
            with open("groups.json", "w") as f:
                json.dump(group_list, f)

# Setup bot
app = ApplicationBuilder().token(TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(CommandHandler("groups", groups))
app.add_handler(CommandHandler("raj", raj))
app.add_handler(CommandHandler("rajkumar", rajkumar))

# Messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

# Group tracking
app.add_handler(ChatMemberHandler(group_tracker, ChatMemberHandler.CHAT_MEMBER))

# Run bot
if __name__ == "__main__":
    print("🤖 Bot is running... powered by @raj_dev_01")
    app.run_polling()

# don't remove credit powered by @raj_dev_01
# don't remove credit powered by @raj_dev_01
