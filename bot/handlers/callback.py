import os

from telegram import Update
from telegram.ext import ContextTypes

from bot.services.downloader import download_video
from config import ALLOWED_USER_IDS


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:
        await query.edit_message_text(
            "❌ Sorry, you're not authorized to use this bot."
        )
        return

    choice = query.data

    # Cancel download
    if choice == "cancel":
        await query.edit_message_text(
            "❌ Download cancelled."
        )
        return

    url = context.user_data.get("video_url")

    if not url:
        await query.edit_message_text(
            "❌ Session expired.\nPlease send the URL again."
        )
        return

    await query.edit_message_text(
        "⬇️ Downloading..."
    )

    try:
        file_path = download_video(url, choice)

        await query.message.reply_text(
            "📤 Uploading..."
        )

        # Send as audio if the user asked for audio-only,
        # otherwise send as a video. Telegram renders these
        # differently (audio gets a proper audio player UI).
        if choice == "audio":
            with open(file_path, "rb") as audio_file:
                await query.message.reply_audio(
                    audio=audio_file,
                    read_timeout=300,
                    write_timeout=300,
                    connect_timeout=60,
                    pool_timeout=60,
                )
        else:
            with open(file_path, "rb") as video_file:
                await query.message.reply_video(
                    video=video_file,
                    read_timeout=300,
                    write_timeout=300,
                    connect_timeout=60,
                    pool_timeout=60,
                )

        if os.path.exists(file_path):
            os.remove(file_path)

        if choice == "audio":
            await query.message.reply_text("✅ Done! Here's your audio file.")
        else:
            await query.message.reply_text(
                "✅ Done! Save this video, then set it as your WhatsApp status."
            )

    except Exception as e:
        await query.message.reply_text(
            f"❌ {str(e)}"
        )