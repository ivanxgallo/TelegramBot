from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from functions import *

# Coloca aquí tu token de acceso proporcionado por BotFather
TOKEN = "6832399374:AAGbQsxgRr8ks83bfwD_EBc1fu-JaJE5028"

def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", starter))
    dispatcher.add_handler(CommandHandler("help", helper))
    dispatcher.add_handler(CommandHandler("players", show_players))

    # Agrega un MessageHandler para analizar todos los mensajes
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, analyzer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()