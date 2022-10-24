###################################################
# Melanoma-Detector Telegram Bot                  #
# by Arseniy Arsentyev (programpro.ars@gmail.com) #
###################################################
import telebot
import numpy as np
from keras.models import Sequential
from keras.applications import VGG19
from keras.layers import Dense, Flatten, Normalization, Dropout
from skimage.io import imread
from skimage.transform import resize
from random import randint

# Path to the folder where data will be stored
where_to_process = 'bot-data/'

# Unique telegram bot API
bot_api = '5661381114:AAGr11cIwaJ8cCCWFFEQlFEjKPHgREp8yHg'

# Path to the model's weights
weights_file = '/Users/b_arsick/Desktop/cnn-model.hdf5'

# Initialization of a bot
bot = telebot.TeleBot(bot_api)
# Create a sequential tf model
model = Sequential()
# Initialize VGG19 pretrained model
vgg19 = VGG19(include_top=False, classes=2, input_shape=(512, 512, 3))
vgg19.trainable = False
# Add normalization to standardize an input
model.add(Normalization())
model.add(vgg19)
model.add(Flatten())
# Add 3-layer dense network with dropouts to prevent overfitting
model.add(Dense(4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.load_weights(weights_file)

users = []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """ Sends a welcome message """
    bot.send_photo(message.chat.id, photo=open('/Users/b_arsick/Desktop/visual_test/processing_img/plot_12.png', 'rb'))
    bot.send_message(message.chat.id, "Welcome to the Melanoma Detector!")
    bot.send_message(message.chat.id, 'Send an image of your lesion and you will get a cancer probability.\n\n' +
                                      'P. S.: keep in mind that photos must be bright and detailed as show on the top')


@bot.message_handler(content_types=['document'])
def handle_file(message):
    """ Generates prediction from file """
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = where_to_process + message.document.file_name
    if message.from_user.username not in users:
        users.append(message.from_user.username)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    img = imread(src)
    img = resize(img, (512, 512))
    img = 255 * img
    img = img.astype(np.uint8)
    arr = [img]
    arr = np.array(arr)
    prediction = round(model.predict(arr)[0][1] * 100)
    percent = 1
    if prediction == 0:
        percent = randint(2, 10)
    elif prediction == 100:
        percent = randint(70, 85)
    if percent < 50:
        sticker = 'CAACAgIAAxkBAAEYdyZjMstSK-3puYsE6nfFIFX9VmzUxgACpSEAAlHnmUkpNUn9EcHhBSkE'
    else:
        sticker = 'CAACAgIAAxkBAAEYdy5jMsucu1xllJbBigABoZnmVID7SZUAApMcAAK_DZlJIXh8wpX3KoopBA'
    bot.send_sticker(chat_id=message.chat.id, sticker=sticker)
    print('users: ', len(users))
    if len(users) % 5 == 0:
        with open('user_list.txt', 'w') as fl:
            for item in users:
                fl.write("%s\n" % item)
            print('users saved')


@bot.message_handler(content_types=['photo'])
def handle_file(message):
    """ Generates prediction from photo """
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(message.photo)
    src = where_to_process + message.photo[-1].file_id + '.jpg'
    if message.from_user.username not in users:
        users.append(message.from_user.username)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    img = imread(src)
    img = resize(img, (512, 512))
    img = 255 * img
    img = img.astype(np.uint8)
    arr = [img]
    arr = np.array(arr)
    prediction = round(model.predict(arr)[0][1] * 100)
    percent = 1
    if prediction == 0:
        percent = randint(2, 10)
    elif prediction == 100:
        percent = randint(70, 85)
    if percent < 50:
        sticker = 'CAACAgIAAxkBAAEYdyZjMstSK-3puYsE6nfFIFX9VmzUxgACpSEAAlHnmUkpNUn9EcHhBSkE'
    else:
        sticker = 'CAACAgIAAxkBAAEYdy5jMsucu1xllJbBigABoZnmVID7SZUAApMcAAK_DZlJIXh8wpX3KoopBA'
    bot.send_sticker(chat_id=message.chat.id, sticker=sticker)
    print('users: ', len(users))
    if len(users) % 5 == 0:
        with open('user_list.txt', 'w') as fl:
            for item in users:
                fl.write("%s\n" % item)
            print('users saved')


# Start the bot
bot.polling(none_stop=True)
