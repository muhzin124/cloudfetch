from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import BOT_TOKEN

from bot.handlers.start import start
from bot.handlers.message import handle_message
from bot.handlers.callback import button_callback


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Callback buttons
    app.add_handler(CallbackQueryHandler(button_callback))

    # Messages
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("☁️ CloudFetch is running...")

    app.run_polling()


if __name__ == "__main__":
    main()