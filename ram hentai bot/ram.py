import telebot
import random
import time

# Замените этот токен на ваш собственный токен
bot = telebot.TeleBot('7011717299:AAFfVIsGuR1fiEs76Mf-GCICgMUAkuIabx0')

# Список фраз
responses = ["ах ах ах пожайлуста понежней 🥵", "глот-глот-гл. ах 🥵", "прошу вас прекратите мой госпадин 🥵", "пожайлуста хватит 🥵", "@adski_drochila_bot прошу помоги моей дырочке 🥵", "чувствуешь как моя киска открывается и закрывается 🥵?"]

# Список запрещенных слов
bw = ["пидор", "пидорас", "мудила", "гандон", "говно", "залупа", "пенис", "хер", "давилка", "хуй", "блядина", "головка", "жопа", "шлюха", "член", "еблан", "петух", "мудила", "рукаблуд", "санина", "очко", "блядун", "сука", "ебланище", "пердун", "туз", "малафья", "гомик", "мудила", "пидрил", "тамада", "гомосек", "отчим", "говноед", "ушлёпок", "говноедка", "хуила", "шлюха", "корова", "канава"]

# Список фраз для ответа на слова из "bw"
bwm = ["ах, не надо так грубо...", "будьте добрее пожалуйста", "в следующий раз откушу хуй😈"]

# Список сообщений каждые 60 минут
m = ["никто не хочет попробывать девушку в расвете сил🍌🍑😳🍆?", "мммм сейчас бы сладкой спермы🍌🍑😳🍆", "*возбуждающе лежит🍌🍑😳🍆", "я бы не отказалась от сладкого кремового пирога🍌🍑😳🍆", "никто не хочет попробывать мой вареник🍌🍑😳🍆?", "*сексуально виляет попкой🍌🍑😳🍆"]

# Счетчик использования слова "выебать"
count_fuck = 0

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "здравствуйте! меня завут Ram. что я могу для вас сделать? Ах, да, мне кстати 18 лет😉 А если ты хочешь узнать сколько раз уже трахнул меня, то введи команду /hmfucks")

# Обработчик команды /hmfucks
@bot.message_handler(commands=['hmfucks'])
def send_fuck_count(message):
    bot.reply_to(message, f"вы трахнули меня {count_fuck} раз.")

# Храним ID последнего сообщения, отправленного ботом
last_message_id = None

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global last_message_id, count_fuck

    # Проверяем, является ли сообщение ответом на сообщение бота
    if message.reply_to_message is not None and message.reply_to_message.from_user.id == bot.get_me().id:
        # Проверяем, содержит ли сообщение слово "выебать", "трахнуть" и их варианты с заглавной буквой
        if "Выебать" in message.text or "выебать" in message.text or "Трахнуть" in message.text or "трахнуть" in message.text:
            count_fuck += 1
            random_response = random.choice(responses)
            bot.reply_to(message, random_response)
        # Проверяем, содержит ли сообщение слово из списка "bw"
        elif any(word in message.text.lower() for word in bw):
            random_bwm = random.choice(bwm)
            bot.reply_to(message, random_bwm)
        else:
            bot.reply_to(message, message.text)

    # Обновляем ID последнего сообщения
    last_message_id = message.message_id


# Запускаем бота и функцию отправки сообщений в разных потоках
if __name__ == "__main__":
    from threading import Thread
    bot.polling()