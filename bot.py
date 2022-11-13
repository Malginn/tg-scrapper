import telebot
from auth_data import token
import requests

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'hi')


    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if 'http' in message.text.lower():
            try:
                bot.send_message(message.chat.id, 'you send me mes')
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'bad answer')
        else:
            bot.send_message(message.chat.id, 'what????')


    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)

