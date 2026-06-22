from config import telegram_token
from telebot import TeleBot
from datetime import datetime
import process
import link_changer
import shortner
import data_uploader

bot = TeleBot(telegram_token)




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}, this bot is started !")



@bot.message_handler(commands=['createmessage'])
def create_message(message):
    bot.send_message(message.chat.id, "enter the link of your movie / video.")
    bot.register_next_step_handler(message, get_name)

myList = []

def get_name(message):
    bot.send_message(message.chat.id, "enter the name of the movie / video.")
    link = link_changer.drive_to_direct(message.text)
    myList.append(link)           # myList[0]
    link_A = shortner.arolinks_shortner(link)
    myList.append(link_A)         # myList[1]
    link_B = shortner.viplinks_url_shortner(link)
    myList.append(link_B)         # myList[2]
    bot.register_next_step_handler(message, get_year)

def get_year(message):
    name = message.text
    myList.append(name)            # myList[3]
    bot.send_message(message.chat.id, "enter the year of the movie / video.")
    bot.register_next_step_handler(message, get_rating)

def get_rating(message):
    year = message.text
    myList.append(year)             # myList[4]
    bot.send_message(message.chat.id, "enter the rating of the movie / video.")
    bot.register_next_step_handler(message, get_language)

def get_language(message):
    rating = message.text
    myList.append(rating)            # myList[5]
    bot.send_message(message.chat.id, "enter the language of the movie / video.")
    bot.register_next_step_handler(message, get_quality)

def get_quality(message):
    language = message.text
    myList.append(language)          # myList[6]
    bot.send_message(message.chat.id, "enter the quality of the movie / video.")
    bot.register_next_step_handler(message, procesing)

def procesing(message):
    lnk = myList[0]
    lnk1 = myList[1]
    lnk2 = myList[2]
    nme = myList[3]
    yer = myList[4]
    rate = myList[5]
    lang = myList[6]
    qualty = message.text
    now = datetime.now()


    output_text = process.process_data(lnk1, lnk2, nme, yer, rate, lang, qualty)
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    bot.send_message(message.chat.id, output_text)
    data_uploader.send_to_spreadsheet(lnk, lnk2, lnk1, nme, yer, rate, lang, qualty, str(now.date()), str(now.time()), firstname, lastname, message.chat.id)












bot.polling()