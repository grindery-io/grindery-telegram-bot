from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import logging
import aiohttp
import os
from dotenv import load_dotenv
from flask import Flask
import threading


load_dotenv()

# TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TOKEN = ''
WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/14479245/35hqzv0/'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
        
async def send_to_webhook(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=data) as response:
            return await response.text()
        
def format_contact_data(data):
    return {
        "user_id": data.chat.id,
        "contact_user_id": data.contact.user_id,
        "contact_first_name": data.contact.first_name,
        "contact_last_name": data.contact.last_name,
        "contact_phone_number": data.contact.phone_number
    }

async def get_shared_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = format_contact_data(data=update.message)
    response = await send_to_webhook(contact)
    print(f"Webhook response: {response}")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    t = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.getenv("PORT") or 3000)))
    t.daemon = True
    t.start()
    application = ApplicationBuilder().token(token=TOKEN).build()
    get_shared_contact_handler = MessageHandler(filters.CONTACT, get_shared_contact)
    application.add_handler(get_shared_contact_handler)
    
    application.run_polling()