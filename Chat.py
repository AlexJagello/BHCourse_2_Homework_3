import telebot
from telebot import types
import requests
import NLPbot
import emoji



bot = telebot.TeleBot('7006022839:AAEnf2iClBJwQNqFty5IvFoegTaSwOK2-OY')

chat_bot = NLPbot.NLPBot()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, "Напишите \"Привет\"")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    answer = chat_bot.getPrediction(message.text)
    if answer == None:
        response = requests.get("https://cataas.com/cat")
        bot.send_photo(message.from_user.id, response.content,caption="Не знаю что ответить. У меня лапки" + 3*emoji.emojize("😿"), reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, answer)

bot.polling(none_stop=True, interval=0)




