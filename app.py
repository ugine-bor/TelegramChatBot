from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram import Update

from dotenv import load_dotenv
from os import getenv

from handlers import start, text
def main():
    load_dotenv()

    application = Application.builder().token(getenv("BOT_TOKEN")).build()


    application.add_handler(CommandHandler("help", start.help))
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("model", start.model))

    application.add_handler(CallbackQueryHandler(start.button))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text.answer))


    print('Г-н Нейросеть запущен')
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    print('Г-н Нейросеть выключен')


if __name__ == "__main__":
    main()
