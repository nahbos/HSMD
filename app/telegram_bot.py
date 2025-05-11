from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

class TelegramBot:
    def __init__(self, token, fastapi_url):
        self.token = token
        self.fastapi_url = fastapi_url

    def start(self, update: Update, _: CallbackContext):
        update.message.reply_text('سلام. سوالت رو بپرس ))')

    def ask_question(self, update: Update, _: CallbackContext):
        question = update.message.text
        try:
            response = requests.post(self.fastapi_url, json={"question": question})
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    answer = json_data.get('answer', 'Sorry, I could not find an answer.')
                except ValueError:
                    answer = 'Sorry, received invalid response format.'
            else:
                answer = f"Error: Received status code {response.status_code}"
        except requests.RequestException as e:
            answer = f"Error: Could not connect to server. {e}"
        update.message.reply_text(answer)

    def run(self):
        updater = Updater(self.token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.ask_question))
        updater.start_polling()
        updater.idle()