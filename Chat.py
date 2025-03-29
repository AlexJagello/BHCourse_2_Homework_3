import telebot
from telebot import types
import requests
import NLPbot
import emoji
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.info('Started')

bot = telebot.TeleBot('7006022839:AAEnf2iClBJwQNqFty5IvFoegTaSwOK2-OY')

chat_bot = NLPbot.NLPBot()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Напишите \"Привет\"")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    answer, prop = chat_bot.getPrediction(message.text)
    logger.info(answer + "  confidence: " + prop.__str__())

    if answer == None or message.text.lower().find("кот") != -1:
        response = requests.get("https://cataas.com/cat")
 
        bot.send_photo(message.from_user.id, response.content,caption=3*emoji.emojize(":cat_face:") + " " + answer + " " + 3*emoji.emojize(":cat_face:"), reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, answer)

bot.polling(none_stop=True, interval=0)




