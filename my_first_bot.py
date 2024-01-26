from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from team_optimazer import *

# Coloca aquí tu token de acceso proporcionado por BotFather
TOKEN = "6832399374:AAGbQsxgRr8ks83bfwD_EBc1fu-JaJE5028"

HELP_TEXT = '''
Este Bot es propiedad de VoludosInk.
Está diseñado para simplificar la
creación de equipos en futbolito.

El modo de uso es la siguiente:
Se debe ingresar una lista numerada de nombres.
Este es un ejemplo de mensaje a ingresar:

1. jugador1
2. jugador2
.
.
.
14. jugador14

Este Bot retornará los equipos más equilibrados que encuentre.
'''

def starter(update, context):
    user = update.effective_user
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hola {user.mention_html()}!',
        parse_mode='HTML',
    )

def helper(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_TEXT)

def analyzer(update, context):
    # Obtén el texto del mensaje
    mensaje = update.message.text

    # Realiza algún tipo de análisis (puedes personalizar esto según tus necesidades)
    resultado_analisis = f"Análisis del mensaje: {mensaje.upper()}"

    # Envía el resultado del análisis como respuesta
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=resultado_analisis
    )

def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", starter))
    dispatcher.add_handler(CommandHandler("help", helper))

    # Agrega un MessageHandler para analizar todos los mensajes
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, analyzer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()