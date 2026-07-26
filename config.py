import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN not found. Please check your .env file."
    )

# -----------------------------
# Allowed users
# -----------------------------
# Comma-separated list of Telegram numeric user IDs allowed to
# use this bot (e.g. "111111111,222222222"). Anyone else who
# messages the bot gets rejected. This matters because Telegram
# bots are publicly discoverable by username by default — without
# this check, a stranger who finds the bot could run up your
# AWS bill or fill your server's disk with downloads.
_allowed_ids_raw = os.getenv("ALLOWED_USER_IDS", "")

ALLOWED_USER_IDS = {
    int(uid.strip())
    for uid in _allowed_ids_raw.split(",")
    if uid.strip().isdigit()
}

if not ALLOWED_USER_IDS:
    raise ValueError(
        "ALLOWED_USER_IDS not found or empty. Please set it in your "
        ".env file, e.g. ALLOWED_USER_IDS=111111111,222222222"
    )
