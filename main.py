import telebot

from random import randint
from datetime import datetime as dt
from database import DB
from telebot import types


TOKEN = '7498702289:AAF6w2T83E1ub2iEiZBZC5BJ7jWX51QWzII'
bot = telebot.TeleBot(TOKEN)
echo = False
current_user = None
di = {}
img_di = {}
answer = ''
LOG = None
name = ''
age = 0
password = ''
DB = DB()

keyboard_home = types.ReplyKeyboardMarkup(resize_keyboard=True)
but_exit = types.KeyboardButton('дай отменить')
but_reg = types.KeyboardButton('хочу зарегаться')
but_profile = types.KeyboardButton('профиль')
but_func = types.KeyboardButton('функции')
keyboard_home.add(but_reg, but_func, but_profile, but_exit)

keyboard_func = types.ReplyKeyboardMarkup(resize_keyboard=True)
but_repeat = types.KeyboardButton('повторяй за мной')
but_no_repeat = types.KeyboardButton('не повторяй за мной')
but_img = types.KeyboardButton('хочу фотку')
but_sticker = types.KeyboardButton('хочу стикер')
keyboard_func.add(but_repeat, but_no_repeat, but_profile, but_img, but_sticker, but_exit)

keyboard_acc = types.ReplyKeyboardMarkup(resize_keyboard=True)
but_acc = types.KeyboardButton('расскажи обо мне')
but_sign_in = types.KeyboardButton('дай войти')
but_sign_out = types.KeyboardButton('дай выйти')
keyboard_acc.add(but_acc, but_sign_in, but_sign_out, but_exit)

keyboard_exit = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_exit.add(but_exit)


@bot.message_handler(commands=['start', 'help'])
def getting_started(message):
    bot.send_message(message.from_user.id, """Вот мои кодовые слова😘:
функции
повторяй за мной
не повторяй за мной
хочу стикер
хочу фотку
хочу зарегаться
расскажи обо мне
дай войти
дай выйти
профиль""")
    bot.send_message(message.from_user.id, "Скажи что-нибудь, любимый!😘")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global echo
    global current_user
    global LOG
    global answer
    answer = ''

    if '/' != message.text[0]:
        if message.text.upper() == 'GIMME YOURSELF':
            bot.send_message(message.from_user.id, 'Всё для тебя любимый😘')
            answer = f'Всё для тебя любимый😘 + {di}'
            print(di)

        elif message.text.lower() == 'повторяй за мной':
            echo = True
            bot.send_message(message.from_user.id, 'Повторяю за тобой😘')
            answer = 'Повторяю за тобой😘'

        elif message.text.lower() == 'не повторяй за мной':
            echo = False
            bot.send_message(message.from_user.id, 'не повторяю за тобой😘')
            answer = 'Но любимый, ты уже зареган, если хочешь перерегаться напиши: "хочу перерегаться"😘'

        elif message.text.lower() == 'хочу зарегаться':
            bot.register_next_step_handler(bot.send_message(message.chat.id, "Как тебя зовут, любимый?(Ф И О)😘"),
                                           set_fio)

        elif message.text.lower() == 'хочу стикер':
            dice = randint(1, 10)
            sticker = open(f'memes/meme{dice}.jpg', 'rb')
            bot.send_sticker(message.chat.id, sticker)
            sticker.close()
            bot.send_message(message.from_user.id, 'Смотри, какой забавный стикер!😘')
            answer = f'Смотри, какой забавный стикер!😘(meme - {dice})'

        elif message.text.lower() == 'хочу фотку':
            if current_user:
                dice = randint(1, 25)
                if not img_di.get(message.chat.id):
                    img_di[message.chat.id] = []
                while dice in img_di.get(message.chat.id):
                    dice = randint(1, 25)
                if not img_di.get(message.chat.id):
                    img_di[message.chat.id] = [dice]
                else:
                    img_di[message.chat.id].append(dice)
                if len(img_di.get(message.chat.id)) >= 25:
                    img_di[message.chat.id] = []
                photo = open(f'img/img{dice}.jpg', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
                bot.send_message(message.from_user.id, 'Надеюсь, я тебе нравлюсь, любимый😘', reply_markup=keyboard_home)
                answer = f'Надеюсь, я тебе нравлюсь, любимый😘(img - {dice})'
            else:
                bot.send_message(message.from_user.id, 'Любимый, ты ещё не вошел в аккаунт😘')
                answer = 'Любимый, ты еще не вошел в аккаунт😭'

        elif message.text.lower() == 'расскажи обо мне':
            if current_user:
                bot.send_message(message.from_user.id, 'Вот все что я знаю о тебе:😘')
                bot.send_message(message.from_user.id, f'Тебя зовут:{di.get(message.chat.id).split(";")[0]}😘')
                bot.send_message(message.from_user.id, f'Тебе {di.get(message.chat.id).split(";")[1]}😘')
                bot.send_message(message.from_user.id, f'Твой пароль:{di.get(message.chat.id).split(";")[2]}😘')
                answer = (f'Вот все что я знаю о тебе:😘\tТебя зовут:{di.get(message.chat.id).split(";")[0]}😘\t'
                          f'Тебе {di.get(message.chat.id).split(";")[1]}😘\t'
                          f'Твой пароль:{di.get(message.chat.id).split(";")[2]}😘')
            else:
                bot.send_message(message.from_user.id, 'Любимый, ты еще не вошел в аккаунт я ничего о тебе не знаю😭')
                answer = 'Любимый, ты еще не вошел в аккаунт я ничего о тебе не знаю😭'

        elif message.text.lower() == 'дай войти':
            if current_user:
                bot.send_message(message.from_user.id, 'Сначала выйди, любимый😘')
                answer = 'Сначала выйди, любимый😘'
            else:
                bot.register_next_step_handler(
                    bot.send_message(message.chat.id, "Любимый, чтобы войти напиши ФИО и пароль😘"),
                    sign_in)

        elif message.text.lower() == 'дай выйти':
            if not current_user:
                bot.send_message(message.from_user.id, 'Любимый, ты и так не вошел в аккаунт😘')
                answer = 'Любимый, ты и так не вошел в аккаунт😘'
            else:
                current_user = None
                bot.send_message(message.from_user.id, f'Любимый, ты вышел из аккаунта😘')
                answer = f'Любимый, ты вышел из аккаунта😘'

        elif message.text.lower() == 'спокойной ночи':
            bot.send_message(message.from_user.id, 'Сладких снов, любимый😘')
            answer = 'Сладких снов, любимый😘'

        elif message.text.lower() == "kys":
            bot.send_message(message.from_user.id, 'За что ты так со мной😭', )
            answer = 'За что ты так со мной😭'

        elif message.text.lower() == 'привет':
            bot.send_message(message.from_user.id, 'Привет, любимый😘')
            answer = 'Привет, любимый😘'

        elif message.text.lower() == 'доброе утро':
            bot.send_message(message.from_user.id, 'Доброе, любимый😘')
            answer = 'Доброе, любимый😘'

        elif echo:
            bot.send_message(message.from_user.id, f"{message.text}😘")
            answer = f"{message.text}😘"

        else:
            bot.send_message(message.from_user.id, "Я всё равно тебя люблю.😘")
            answer = "Я всё равно тебя люблю.😘"

    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.message_handler(content_types=['text'])
def sign_in(message):
    global answer
    global current_user
    global LOG
    if ' '.join(message.text.split()) == ' '.join(di.get(message.chat.id).split(';')):
        current_user = DB.sign_in(message.text.split())
        bot.send_message(message.from_user.id, f'Любимый, ты вошел как: Пользователь {current_user}😘')
        answer = f'Любимый, чтобы войти напиши ФИО и пароль😘\tЛюбимый, ты вошел как: Пользователь {current_user}😘'
    elif len(message.text.split()) != 4:
        answer = f'Любимый, чтобы войти напиши ФИО и пароль😘\tЯ тебя не поняла, неверный формат😭'
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Я тебя не поняла, неверный формат😭"), sign_in)
    elif ' '.join(message.text.split()) != ' '.join(di.get(message.chat.id).split(';')):
        answer = f'Любимый, чтобы войти напиши ФИО, и пароль😘\tНеверные данные, любимый😭'
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Неверные данные, любимый😭"), sign_in)
    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.message_handler(content_types=['text'])
def set_fio(message):
    global answer
    global LOG
    global name
    if len(message.text.split()) == 3:
        bot.send_message(message.chat.id, f'У тебя такое красивое имя: {message.text}😘')
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'А сколько тебе лет, любимый?😘'), set_age)
        answer = (f"Как тебя зовут, любимый?(Ф И О)😘\tУ тебя такое красивое имя: {message.text}😘"
                  f"\t А сколько тебе лет, любимый?😘")
        di[message.chat.id] = message.text
        name = message.text
    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Я тебя не поняла, неверный формат😭"), set_fio)
        answer = "Как тебя зовут, любимый?(Ф И О)😘\tЯ тебя не поняла, неверный формат😭"
    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.message_handler(content_types=['text'])
def set_password(message):
    global answer
    global current_user
    global LOG
    global name, age, password
    try:
        password = str(message.text)
        if len(message.text.split()) > 1:
            raise ValueError
        print(name, age, password)
        DB.insert_noob([name, age, password])
        print(1)
        current_user = DB.sign_in([name, password])
        answer = f'Теперь твой пароль: {message.text}😘\tЛюбимый, ты вошел как: Пользователь {current_user}😘'
        bot.send_message(message.chat.id, f'Теперь твой пароль: {message.text}😘')
        bot.send_message(message.chat.id, f'Любимый, ты вошел как: Пользователь {current_user}😘')
        LOG = open('log.txt', 'a')
        LOG.write(
            f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')
    except:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Я тебя не поняла, неверный формат😭"),
                                       set_password)
        answer = "Я тебя не поняла, неверный формат😭"
        LOG = open('log.txt', 'a')
        LOG.write(
            f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')
        return


@bot.message_handler(content_types=['text'])
def set_age(message):
    global answer
    global LOG
    global age
    try:
        age_ = int(message.text)
        di[message.chat.id] += f';{message.text}'
        if age_ < 18:
            bot.send_message(message.chat.id, f'Ты еще такой маленький😘')
        elif 18 <= age_ <= 20:
            bot.send_message(message.chat.id, f'Ого, мой ровесник😘')
        elif age_ > 20:
            bot.send_message(message.chat.id, f'Ого, ты старше меня😘')
        bot.register_next_step_handler(bot.send_message(message.chat.id,
                                                        "Наконец, любимый, придумай надежный пароль😘(Без пробелов)"),
                                       set_password)
        answer = "f'Ого, мой ровесник😘'\tНаконец, любимый, придумай надежный пароль😘"
        age = age_
        LOG = open('log.txt', 'a')
        LOG.write(
            f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')
    except:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Я тебя не поняла, неверный формат😭"),
                                       set_age)
        answer = "Я тебя не поняла, неверный формат😭"
        LOG = open('log.txt', 'a')
        LOG.write(
            f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')
        return


@bot.message_handler(content_types=['photo', 'audio', 'video', 'video_note'])
def get_pretty_messages(message):
    global LOG
    global answer
    bot.send_message(message.from_user.id, "Как красиво!😘")
    answer = "Как интересно!😘"
    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.message_handler(content_types=['document'])
def get_smart_messages(message):
    global LOG
    global answer
    bot.send_message(message.from_user.id, "Как интересно!😘")
    answer = "Как интересно!😘"
    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.message_handler(content_types=['sticker'])
def get_sticker_messages(message):
    global LOG
    global answer
    bot.send_message(message.from_user.id, "У тебя такие классные стикеры!😘")
    answer = "У тебя такие классные стикеры!😘"
    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: @{message.from_user.username}: {message.text} - {answer}\n')


bot.infinity_polling()
