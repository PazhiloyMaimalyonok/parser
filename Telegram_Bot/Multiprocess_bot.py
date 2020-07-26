#import config
import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token='1386333187:AAEdLI9emOBGG-bwC3wgoauiLsiPWC2hIGg')
dp = Dispatcher(bot)

with open('users.txt', 'r') as f:
    users = f.read().splitlines()
users = set(users)
@dp.message_handler(commands=['start'])
async def add_user(message):
    if not str(message.from_user.id) in users:
        with open('users.txt', 'a') as f:
            f.write(str(message.from_user.id) + '\n')
        users.add(message.from_user.id)
        await bot.send_message(message.from_user.id, 'У меня есть твои данные. АХАХАХАХАХА')

@dp.message_handler(content_types=['text'])
async def get_text_messages(message):

    if message.text == "Привет":

        await bot.send_message(message.from_user.id, "Привет, я родился")

    elif message.text == "/help":

        await bot.send_message(message.from_user.id, "Напиши Привет")

    else:

        await bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


async def scheduled(wait_for):
    global users
    left_users = set()
    while True:
        await asyncio.sleep(wait_for)
        for user in users:
            try:
                await bot.send_message(user, 'Ура,работает')
            except:
                left_users.add(user)
        users = users.difference(left_users)
        #with open('users.txt', 'w') as f:
            #for user in users:
                #f.write(str(user) + '\n')


if __name__ == '__main__':
	dp.loop.create_task(scheduled(10)) # пока что оставим 10 секунд (в качестве теста)
	executor.start_polling(dp, skip_updates=True)
