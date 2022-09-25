###################################################
# Melanoma-Detector Bot                           #
# by Arseniy Arsentyev (programpro.ars@gmail.com) #
###################################################
import telebot

bot_api = open('secure_data.txt')
bot = telebot.TeleBot(bot_api.readlines()[0])
bot_api.close()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Please, send an image")


@bot.message_handler(content_types=['document'])
def handle_file(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = '/Users/b_arsick/Desktop/' + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


@bot.message_handler(content_types=['photo'])
def handle_file(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = '/Users/b_arsick/Desktop/res.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


bot.infinity_polling()
