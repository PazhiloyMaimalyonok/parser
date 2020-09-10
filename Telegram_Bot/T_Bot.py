#import config
import logging
import asyncio
import rassylka
from datetime import datetime
from aiogram import Bot, Dispatcher, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import emoji
import pickle
SMILES = ['✅', '❎']

bot = Bot(token='1386333187:AAEdLI9emOBGG-bwC3wgoauiLsiPWC2hIGg')
dp = Dispatcher(bot)

with open('users.txt', 'r') as f:
    users = f.read().splitlines()
users = set(users)
@dp.message_handler(commands=['start'])
async def add_user(message):
    if not str(message.chat.id) in users:
        with open('users.txt', 'a') as f:
            f.write(str(message.chat.id) + '\n')
        users.add(message.chat.id)
        await bot.send_message(message.chat.id, f'Привет, я дружелюбный бот SentiMetr от команды https://www.sentimetrica.ru/ . Мои создатели с помощью искусственного интеллекта анализируют настроение трейдеров для принятия грамотных инвестиционных решений. Я буду присылать тебе ежедневную информацию об изменениях и состоянии портфеля. Если остались вопросы - пиши /help ')

button1 = KeyboardButton('Контакты')
button2 = KeyboardButton('Текущий портфель')
button3 = KeyboardButton('Сайт')
#button3 = KeyboardButton('Нашел баг')
markup3 = ReplyKeyboardMarkup().add(
    button1).add(button3).add(button2)
@dp.message_handler(commands=['help'])
async def add_user(message):
    await message.reply("Вот, что я умею", reply_markup=markup3)

@dp.message_handler(content_types=['text'])
async def get_text_messages(message):

    if message.text == "Контакты":

        await bot.send_message(message.chat.id, "@atomtosov")

    elif message.text == "Текущий портфель":

        with open("/home/danyanyam/flask/Библиотека/data/pickles/portfel.pickle", "rb") as fobj:
            data = pickle.load(fobj)
        last_update_of_portfolio, amount_of_deals_this_month, cumulated_yield, mean_yield, volatility, musor = \
        data['current_conditions'][0].values()
        stock_list = ''
        for x in musor:
            stock_list += x['ticker'] + ', '
        stock_list = stock_list[:-2]
        await bot.send_message(message.chat.id, f"Текущий портфель: {stock_list} \nХарактеристика портфеля: Совокупная доходность = {cumulated_yield* 100} %, количество сделок за месяц = {amount_of_deals_this_month}, волатильность = {volatility*100}%")

    elif message.text == "Сайт":

        await bot.send_message(message.chat.id, "На сайте есть статьи нашей команды, а так же текущий портфель.\n https://www.sentimetrica.ru/ ")
    else:
        await bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help")


async def scheduled(wait_for):
    done = False
    global users
    left_users = set()
    last_date = datetime.now().date()
    last_sell_date = None
    last_buy_date = None
    while True:
        await asyncio.sleep(wait_for)
        if datetime.now().date() != last_date:
            done = False
            last_date = datetime.now().date()
        if done == True:
            continue
        a = rassylka.soobschenye()
        if a == False:
            continue
        #b - это сообщение юзерам
        b = ''
        for el in a[0]:
            b += el
        for user in users:

            try:
                await bot.send_message(user, b)
            except:
                left_users.add(user)

            #await bot.send_message(user, b)
        users = users.difference(left_users)

        with open('users.txt', 'w') as f:
            for user in users:
                f.write(str(user) + '\n')
        done = True




if __name__ == '__main__':
	dp.loop.create_task(scheduled(60*30)) # пока что оставим 10 секунд (в качестве теста)
	executor.start_polling(dp, skip_updates=True)
