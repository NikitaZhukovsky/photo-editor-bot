from PIL import Image

import telebot
from telebot import types

TOKEN = 'YOUR TOKEN'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    some_btn = types.KeyboardButton('Редактор фотографий')
    markup.add(some_btn)
    bot.send_message(message.chat.id, 'Нажмите "Редактор фотографий"', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Редактор фотографий")
def photo_editor_options(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    filter_one = types.KeyboardButton('Серый фильтр')
    filter_two = types.KeyboardButton('Растягивание')
    markup.add(filter_one, filter_two)
    bot.send_message(message.chat.id, 'Загрузите фотографию', reply_markup=markup)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     sender_info = f"От: {message.from_user.first_name} {message.from_user.last_name} (ID: {message.from_user.id})"
#     bot.send_message(525820323, f"{sender_info}\n\n{message.text}")
#

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('photo.jpg', 'wb') as photo:
        photo.write(downloaded_file)

    bot.send_message(message.chat.id, "Фотография успешно загружена!")


@bot.message_handler(func=lambda message: message.text == "Серый фильтр")
def apply_gray_filter(message):
    with Image.open('photo.jpg') as img:
        img = img.convert('L')
        img.save('gray_photo.jpg')

    with open('gray_photo.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: message.text == "Растягивание")
def apply_stretch_filter(message):
    with Image.open('photo.jpg') as img:
        width, height = img.size
        new_width = int(width * 4)
        new_height = int(height * 5)
        resized_img = img.resize((new_width, new_height), resample=Image.BILINEAR)
        resized_img.save('stretch_photo.jpg')

    with open('stretch_photo.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.polling(non_stop=True)
