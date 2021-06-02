import telebot
import config
import datetime
import pytz
import json
import traceback

# P_TIMEZONE = pytz.timezone(config.TIMEZONE)
# TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME

bot = telebot.TeleBot(config.TOKEN)


# bot.polling(none_stop=True)

@bot.message_handler(commands=["start", "help"])
def start_command(message):
    bot.send_message(message.chat.id, 'Тест!!!!')


bot.polling()

# bot.reply_to(message, "Howdy, how are you doing?")

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")


# import telebot
#
# bot = telebot.TeleBot("TOKEN")
#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?")
#
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)
#
# bot.polling()
