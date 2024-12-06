import telebot, os
from telebot import types
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в систему бронирования гостиницы!\n"
                          "Введите желаемую дату и время заселения (например, '2023-12-31 15:00').")
    bot.register_next_step_handler(message, process_time_step)

def process_time_step(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'time': message.text}
    bot.send_message(chat_id, "Отлично! Теперь введите тип апартаментов.")
    bot.register_next_step_handler(message, process_apartments_step)

def process_apartments_step(message):
    chat_id = message.chat.id
    user_data[chat_id]['apartments'] = message.text
    bot.send_message(chat_id, "Хорошо! Добавьте дополнительные комментарии, если необходимо, или напишите 'Нет'.")
    bot.register_next_step_handler(message, process_comments_step)

def process_comments_step(message):
    chat_id = message.chat.id
    comments = message.text
    if comments.lower() == 'нет':
        comments = 'Без комментариев'
    user_data[chat_id]['comments'] = comments

    booking_info = (
        f"Ваше бронирование завершено.\n"
        f"Время: {user_data[chat_id]['time']}\n"
        f"Апартаменты: {user_data[chat_id]['apartments']}\n"
        f"Комментарии: {user_data[chat_id]['comments']}\n"
        f"Спасибо за использование нашего сервиса!"
    )

    bot.send_message(chat_id, booking_info)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Пожалуйста, начните с команды /start для бронирования.")

bot.polling(none_stop=True, interval=0)