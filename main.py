import telebot

from random import randint
from datetime import datetime as dt
from telebot import types

TOKEN = '7498702289:AAF6w2T83E1ub2iEiZBZC5BJ7jWX51QWzII'
bot = telebot.TeleBot(TOKEN)
echo = False
current_user = None
di = {}
answer = ''
LOG = None


@bot.message_handler(commands=['start', 'help'])
def getting_started(message):
    bot.send_message(message.from_user.id, """Вот мои кодовые слова😘:
повторяй за мной
не повторяй за мной
хочу стикер
хочу фотку
хочу зарегаться
хочу перерегаться
расскажи обо мне
дай войти
дай выйти""")
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
            dice = randint(1, 25)
            photo = open(f'img/img{dice}.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
            photo.close()
            bot.send_message(message.from_user.id, 'Всё для тебя любимый😘')
            answer = f'Всё для тебя любимый😘(img - {dice}) + {di}'
            print(di)

        elif message.text.lower() == 'повторяй за мной':
            echo = True
            bot.send_message(message.from_user.id, 'Повтооряю за тобой😘')
            answer = 'Повтооряю за тобой😘'

        elif message.text.lower() == 'не повторяй за мной':
            echo = False
            bot.send_message(message.from_user.id, 'Повтооряю за тобой😘')
            answer = 'Но любимый, ты уже зареган, если хочешь перерегаться напиши: "хочу перерегаться"😘'

        elif message.text.lower() == 'хочу зарегаться':
            if not di.get(message.chat.id) and not current_user:
                bot.register_next_step_handler(bot.send_message(message.chat.id, "Как тебя зовут, любимый?(Ф И О)😘"),
                                               set_fio)
            else:
                bot.send_message(message.from_user.id,
                                 'Но любимый, ты уже зареган, если хочешь перерегаться напиши: "хочу перерегаться"😘')
                answer = 'Но любимый, ты уже зареган, если хочешь перерегаться напиши: "хочу перерегаться"😘'

        elif message.text.lower() == 'хочу перерегаться':
            if di.get(message.chat.id) and current_user:
                bot.register_next_step_handler(
                    bot.send_message(message.chat.id, "Как тебя зовут по новому, любимый?(Ф И О)😘"), set_fio)
                answer = 'Как тебя зовут по новому, любимый?(Ф И О)😘'
            else:
                bot.send_message(message.from_user.id,
                                 'Но любимый, ты ещё не зареган, если хочешь заререгаться напиши: "хочу зарегаться"😘')
                answer = 'Но любимый, ты ещё не зареган, если хочешь заререгаться напиши: "хочу зарегаться"😘'

        elif message.text.lower() == 'хочу стикер':
            dice = randint(1, 10)
            sticker = open(f'memes/meme{dice}.jpg', 'rb')
            bot.send_sticker(message.chat.id, sticker)
            sticker.close()
            bot.send_message(message.from_user.id, 'Смотри, какой забавный стикер!😘')
            answer = 'Смотри, какой забавный стикер!😘(meme - {dice})'

        elif message.text.lower() == 'хочу фотку':
            if current_user:
                dice = randint(1, 25)
                photo = open(f'img/img{dice}.jpg', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
                bot.send_message(message.from_user.id, 'Надеюсь, я тебе нравоюсь, любимый😘')
                answer = f'Надеюсь, я тебе нравоюсь, любимый😘(img - {dice})'
            else:
                bot.send_message(message.from_user.id, 'Любимый, ты ещё не вошел в аккаунт😘')
                answer = 'Любимый, ты еще не вошел в аккаунт я ничего о тебе не знаю😭'

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
                    bot.send_message(message.chat.id, "Любимый, чтобы войти напиши ФИО, возраст и пароль😘"),
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
            bot.send_message(message.from_user.id, 'За что ты так со мной😭')
            answer = 'За что ты так со мной😭'

        elif message.text.lower() == 'привет':
            bot.send_message(message.from_user.id, 'Привет, любимый😘')
            answer = 'Привет, любимый😘'

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
    print(' '.join(message.text.split()), ' '.join(di.get(message.chat.id).split(';')))
    if ' '.join(message.text.split()) == ' '.join(di.get(message.chat.id).split(';')):
        current_user = di.get(message.chat.id)[0]
        bot.send_message(message.from_user.id, f'Любимый, ты вошел как: {current_user}😘')
        answer = f'Любимый, чтобы войти напиши ФИО, возраст и пароль😘\tЛюбимый, ты вошел как: {current_user}😘'
    elif len(message.text.split()) != 5:
        print(message.text.split())
        answer = f'Любимый, чтобы войти напиши ФИО, возраст и пароль😘\tЯ тебя не поняла, неверный формат😭'
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Я тебя не поняла, неверный формат😭"), sign_in)
    elif ' '.join(message.text.split()) != ' '.join(di.get(message.chat.id).split(';')):
        answer = f'Любимый, чтобы войти напиши ФИО, возраст и пароль😘\tНеверные данные, любимый😭'
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Неверные данные, любимый😭"), sign_in)
    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.message_handler(content_types=['text'])
def set_fio(message):
    global answer
    global LOG
    if len(message.text.split()) == 3:
        bot.send_message(message.chat.id, f'У тебя такое красивое имя: {message.text}😘')
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'А сколько тебе лет, любимый?😘'), set_age)
        answer = (f"Как тебя зовут, любимый?(Ф И О)😘\tУ тебя такое красивое имя: {message.text}😘"
                  f"\t А сколько тебе лет, любимый?😘")
        di[message.chat.id] = message.text
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
    current_user = di.get(message.chat.id).split(";")[0]
    try:
        str(message.text)
        if len(message.text.split()) > 1:
            raise ValueError
        bot.send_message(message.chat.id, f'Теперь твой пароль: {message.text}😘')
        bot.send_message(message.chat.id, f'Любимый, ты вошел как: {current_user}😘')
        di[message.chat.id] += f';{message.text}'
        answer = f'Теперь твой пароль: {message.text}😘\tЛюбимый, ты вошел как: {current_user}😘'
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
    try:
        age = int(message.text)
        di[message.chat.id] += f';{message.text}'
        if age < 18:
            bot.send_message(message.chat.id, f'Ты еще такой маленький😘')
        elif 18 <= age <= 20:
            bot.send_message(message.chat.id, f'Ого, мой ровесник😘')
        elif age > 20:
            bot.send_message(message.chat.id, f'Ого, ты старше меня😘')
        bot.register_next_step_handler(bot.send_message(message.chat.id,
                                                        "Наконец, любимый, придумай надежный пароль😘(Без пробелов)"),
                                       set_password)
        answer = "f'Ого, мой ровесник😘'\tНаконец, любимый, придумай надежный пароль😘"
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
    bot.send_message(message.from_user.id, "У тебя такие смешные стикеры!😘")
    answer = "У тебя такие смешные стикеры!😘"
    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: @{message.from_user.username}: {message.text} - {answer}\n')


bot.infinity_polling()
