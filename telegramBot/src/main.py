import os

from dotenv import load_dotenv
import telebot

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler()
def send_echo(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)