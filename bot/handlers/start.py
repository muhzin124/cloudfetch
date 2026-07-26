from telegram import Update
from telegram.ext import ContextTypes

from config import ALLOWED_USER_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text(
            "❌ Sorry, you're not authorized to use this bot."
        )
        return

    await update.message.reply_text(
        "☁️ Welcome to CloudFetch!\n\n"
        "Send me a video link from YouTube, Instagram, Facebook, "
        "TikTok, X, Reddit, Vimeo, and most other video sites.\n\n"
        "I'll download it for you."
    )
