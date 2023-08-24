from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import logging
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('FLOW_XO_WEBHOOK_URL')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def send_to_webhook(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=data) as response:
            return await response.text()
        
def format_contact_data(contact):
    return {
        "user_id": contact.user_id,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "phone_number": contact.phone_number
    }

async def get_shared_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = format_contact_data(contact=update.message.contact)    
    response = await send_to_webhook(contact)
    print(f"Webhook response: {response}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(token=TOKEN).build()
    
    get_shared_contact_handler = MessageHandler(filters.CONTACT, get_shared_contact)
    application.add_handler(get_shared_contact_handler)
    
    application.run_polling()
