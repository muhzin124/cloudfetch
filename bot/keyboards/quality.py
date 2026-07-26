from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def quality_keyboard(platform: str):
    """
    Two simple choices: download the video, or extract just
    the audio. Still one tap either way — easy for
    non-technical users (e.g. a parent who just wants to send
    a link and get a video/audio file back).
    """

    keyboard = [
        [
            InlineKeyboardButton("⬇️ Download Video", callback_data="best"),
        ],
        [
            InlineKeyboardButton("🎵 Audio Only", callback_data="audio"),
        ],
        [
            InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
