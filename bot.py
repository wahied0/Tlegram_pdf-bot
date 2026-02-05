import os
from flask import Flask, request
import telebot

# Environment Variables
TOKEN = os.getenv("oken")        # التوكن من BotFather
PASSWORD = os.getenv("PASSWORD") # الباسورد الخاص بك

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

PDF_FOLDER = "pdfs"  # مجلد ملفات PDF

# دالة لإرجاع PDF اليوم
def get_today_pdf():
    from datetime import datetime
    today = datetime.now().day
    file_name = f"day{today}.pdf"
    file_path = os.path.join(PDF_FOLDER, file_name)
    return file_path if os.path.exists(file_path) else None

# الرد على /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً 👋\nادخلي الباسورد يا هبتي 🔐")

# التحقق من الباسورد
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
        bot.send_message(message.chat.id, "❌ الباسورد غلط")

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# صفحة اختبار بسيطة
@app.route("/")
def index():
    return "Bot is running!"

# ضبط Webhook
bot.remove_webhook()
bot.set_webhook(url=f"https://mytelegrambot.up.railway.app/{TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
