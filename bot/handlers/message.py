import os

from telegram import Update
from telegram.error import TimedOut
from telegram.ext import ContextTypes
import validators

from bot.services.platform_detector import detect_platform
from bot.services.downloader import (
    get_video_info,
    download_video,
)

from bot.keyboards.quality import quality_keyboard
from config import ALLOWED_USER_IDS


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text(
            "❌ Sorry, you're not authorized to use this bot."
        )
        return

    # Get user's message
    message = update.message.text.strip()

    # Validate URL
    if not validators.url(message):
        await update.message.reply_text(
            "❌ Please send a valid video URL."
        )
        return

    # Detect platform
    platform = detect_platform(message)

    if platform is None:
        await update.message.reply_text(
            "❌ Unsupported website."
        )
        return

    try:
        # Save URL temporarily
        context.user_data["video_url"] = message
        context.user_data["platform"] = platform

        await update.message.reply_text(
            "🔍 Fetching video information..."
        )

        info = get_video_info(message)

        title = info.get("title", "Unknown Title")
        duration = info.get("duration")

        if duration:
            duration = int(duration)
            minutes = duration // 60
            seconds = duration % 60
            duration_text = f"{minutes}:{seconds:02d}"
        else:
            duration_text = "Unknown"

        await update.message.reply_text(
            f"🎬 Platform: {platform}\n"
            f"📹 Title: {title}\n"
            f"⏱ Duration: {duration_text}"
        )

        # Show download button
        await update.message.reply_text(
            "🎥 Ready to download:",
            reply_markup=quality_keyboard(platform)
        )

    except TimedOut:
        await update.message.reply_text(
            "❌ Request timed out."
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Failed to process the video.\n\n{str(e)}"
        )