from google import genai
from app.document_handler import DocumentHandler
from app.telegram_bot import TelegramBot
from app.api import start_api
from cryptography.fernet import Fernet
import asyncio
import json
import os


async def main():
    # Load key and encrypted secrets
    with open("secret.key", "rb") as kf:
        key = kf.read()

    with open("secrets.enc", "rb") as ef:
        encrypted_data = ef.read()

    # Decrypt
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data)
    secrets = json.loads(decrypted.decode())

    api_key = secrets["API_KEY"]
    telegram_token = secrets["TELEGRAM_TOKEN"]
    data_folder = './data/'

    client = genai.Client(api_key=api_key)

    document_handler = DocumentHandler(client, data_folder)
    await document_handler.load_documents()
    await document_handler.index_documents()

    start_api(document_handler, client)

    telegram_bot = TelegramBot(telegram_token, 'http://localhost:8000/ask')
    telegram_bot.run()

if __name__ == "__main__":
    asyncio.run(main())