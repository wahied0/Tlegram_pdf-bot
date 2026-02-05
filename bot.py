import telebot
from datetime import datetime
import os

TOKEN = os.getenv("oken")      # الاسم زي ما هو في GitHub Secret
PASSWORD = os.getenv("PASSWORD")

PDF_FOLDER = "pdfs"

bot = telebot.TeleBot(TOKEN)
print("Bot started... waiting for messages")

def get_today_pdf():
    today = datetime.now().day
    file_name = f"day{today}.pdf"
    file_path = os.path.join(PDF_FOLDER, file_name)
    if os.path.exists(file_path):
        return file_path
    else:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً 👋\nادخلي الباسورد يا هبتي 🔐")

@bot.message_handler(func=lambda m: True)
def check_password(message):
    if message.text == PASSWORD:
        pdf_file = get_today_pdf()
        if pdf_file:
            with open(pdf_file, "rb") as f:
                bot.send_document(message.chat.id, f)
        else:
            bot.send_message(message.chat.id, "لا يوجد PDF لليوم 🤍")
    else:
       bot.send_message(message.chat.id, """❌ الباسورد غلط""")
