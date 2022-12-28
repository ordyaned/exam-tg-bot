try:
    import sys
    import telebot
    from time import sleep
    from utils import random_question
except ImportError as e:
    print("Please install necessary module(s): {}".format(e))
    sys.exit(1)


bot = telebot.TeleBot('5070510034:AAFDeoB4ImDT7tRQ9Kxge2M7RpU1HfqJg3k')


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I will help you while @ordyaned is busy. To see all commands list type /help")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    commands = """ /start      /question
            /help       /quit """
    bot.send_message(message.chat.id, str(commands))


@bot.message_handler(commands=['question'])
def qnum_handler(message):
    text = "How many questions do you have in your questionnaire?"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, interval_handler)


def interval_handler(message):
    qnum = int(message.text)
    text = "In how many minutes should I send you next question number?".format('\n')
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_number, qnum)


def fetch_number(message, qnum):
    i = 1
    given_numbers = []
    interval = int(message.text)
    while i <= qnum:
        next_question = random_question(qnum)
        while next_question in given_numbers:
            next_question = random_question(qnum)

        given_numbers.append(next_question)
        bot.send_message(message.chat.id, "Your next question is: {}".format(str(next_question)))
        sleep(interval * 60)
    bot.send_message(message.chat.id, "You have completed your questionnaire. Congrats !!!")


@bot.message_handler(commands=['quit'])
def exit_bot(message):
    bot.reply_to(message, "Getting some sleep is also important {} Bye )) Good luck for tomorrow!".format('\n'))
    bot.stop_polling()


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "I don't know yet what does this mean [{}]".format(message.text))


bot.infinity_polling(timeout=10, long_polling_timeout=5)
