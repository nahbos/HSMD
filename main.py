import google.generativeai as genai
from app.document_handler import DocumentHandler
from app.telegram_bot import TelegramBot
from app.api import start_api

def main():
    api_key = 'AIzaSyBh1YfCrOzouS8DqrAwGx0t_vtQGdowOFA'
    telegram_token = '7691048418:AAGy8gsDMODgeBaoaPbiMl8YSl14TJXgtQc'
    data_folder = './data/'

    client = genai.Client(api_key=api_key)

    document_handler = DocumentHandler(client, data_folder)
    document_handler.load_documents()
    document_handler.index_documents()

    start_api(document_handler, client)

    telegram_bot = TelegramBot(telegram_token, 'http://localhost:8000/ask')
    telegram_bot.run()

if __name__ == "__main__":
    main()