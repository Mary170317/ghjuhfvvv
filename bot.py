import telebot
from telebot import types
from config import TOKEN
from datetime import datetime
import openpyxl
import os



API_TOKEN = "8162888826:AAGKQKaqg4WC1FklPmLcw_OGHqjd2O25FbY"
bot = telebot.TeleBot("8162888826:AAGKQKaqg4WC1FklPmLcw_OGHqjd2O25FbY")

language_links = {
    "Python": "https://t.me/pythonvideo",
    "JavaScript": "https://t.me/JS_per_month",
    "Java": "https://t.me/javazavr",
    "C++": "https://t.me/cplusplus_tg"
}

excel_file = 'users_data.xlsx'


if not os.path.exists(excel_file):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "logs"
    ws.append(["Дата и время", "User id", "Имя", "Действие"])
    wb.save(excel_file)


def log_to_excel(user_id, full_name, action):
    try:
        wb = openpyxl.load_workbook(excel_file)
        ws = wb["logs"]
        ws.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, full_name, action])
        wb.save(excel_file)
    except Exception as e:
        print(f"Ошибка при записи в Excel: {e}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lang in language_links:
        markup.add(lang)
    bot.send_message(message.chat.id,
                     "Привет! Я LangLearnBot. Выбери язык программирования, чтобы перейти в обучающий канал:",
                     reply_markup=markup)
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    log_to_excel(message.from_user.id, full_name, "Зашёл в бота (/start)")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = ("Я помогаю находить обучающие Telegram-каналы по языкам программирования.\n"
                 "Нажмите на язык из меню — и получите ссылку.\n"
                 "Доступные команды:\n"
                 "/start — начать\n"
                 "/help — справка")
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: True)
def handle_language_selection(message):
    lang = message.text.strip()
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    if lang in language_links:
        bot.send_message(message.chat.id, f"Вот канал по {lang}: {language_links[lang]}")
        log_to_excel(message.from_user.id, full_name, f"Перешёл в канал {lang}")
    else:
        bot.send_message(message.chat.id, "Я не понял. Пожалуйста, выбери язык из списка.")

bot.infinity_polling()






