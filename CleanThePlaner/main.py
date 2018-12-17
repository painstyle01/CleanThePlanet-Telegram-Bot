# May the force be with you> pain
import sqlite3
import telebot
from telebot import types

# Databases + cursors
main_db = sqlite3.connect('db/main.db', check_same_thread=False)
main_c = main_db.cursor()
location_db = sqlite3.connect('db/locations.db', check_same_thread=False)
location_c = location_db.cursor()

bot = telebot.TeleBot('782969313:AAHtWtT2o8vsKnTjqYplEmmYF5lTs6KMrUs')  # Token

# Keyboard section
main_keyboard = types.ReplyKeyboardMarkup(True)
main_keyboard.row('')

confirm = types.ReplyKeyboardMarkup(True)
confirm.row('Так', "Ні")


def save():
    main_db.commit()
    location_db.commit()


@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        main_c.execute("SELECT * FROM main WHERE id=" + str(message.chat.id))
        p = main_c.fetchone()
        if p[0] is None:
            bot.send_message(message.chat.id, 'Profile', reply_markup=main_keyboard)
    except:
        bot.send_message(message.chat.id, 'Welcome message. Register in process', reply_markup=main_keyboard)
        main_c.execute("INSERT INTO main VALUES ('" + str(message.chat.id) + "','0','0','0')")
        save()


@bot.message_handler(content_types=['location'])
def location_handler(message):
    print(message.location)
    print(message.venue)
    location_c.execute("INSERT INTO locations() VALUES ()")


@bot.message_handler(content_types=['text'])
def text_handler(message):
    main_c.execute("SELECT status FROM main WHERE id=" + str(message.chat.id))
    p = main_c.fetchone()
    if p[0] == 0:
        bot.send_message(message.chat.id, 'You have been banned.')
    if p[0] == 1:
        if message.text == '👤Профіль':
            bot.send_message(message.chat.id, 'Profile')
        if message.text == "Отримати об'єкт для прибирання":
            bot.send_message(message.chat.id, 'Cleaning rules. Reply accept keyboard.', reply_markup=confirm)
            main_c.execute("UPDATE main SET status=2 WHERE id=" + str(message.chat.id))
            save()
        if message.text == 'Чати':
            bot.send_message(message.chat.id, "Cleaners chat")
        if message.text == 'Повідомити про бруд':
            bot.send_message(message.chat.id, 'W8 4 geolocation.')
    if p[0] == 2:
        if message.text == 'Так':
            bot.send_message(message.chat.id, 'Sending random location, adding to bd')
        if message.text == 'Ні':
            bot.send_message(message.chat.id, 'No')


if __name__ == '__main__':
    try:
        bot.polling(True)
    except Exception as e:
        print(e)
        bot.send_message(357572186, 'Exception!!!\n' + str(e))
        bot.polling(True)
