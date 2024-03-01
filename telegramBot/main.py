from os import getenv
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import handlers


def main() -> None:
    load_dotenv()
    print('launch the bot')
    application = Application.builder().token(getenv('BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.echo))

    print('successful launch')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
