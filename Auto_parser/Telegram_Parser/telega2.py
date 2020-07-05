import configparser
import json
import time
import datetime as abc
from telethon.sync import TelegramClient
from telethon import connection
import os
# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

#proxy = (proxy_server, proxy_port, proxy_key)

client = TelegramClient(username, api_id, api_hash)

client.start()


async def dump_all_messages(channel):
	"""Записывает json-файл с информацией о всех сообщениях канала/чата"""
	offset_msg = 0    # номер записи, с которой начинается считывание
	limit_msg = 100   # максимальное число записей, передаваемых за один раз
	all_messages = []   # список всех сообщений
	total_messages = 0
	total_count_limit = 20  # поменяйте это значение, если вам нужны не все сообщения

	class DateTimeEncoder(json.JSONEncoder):
		'''Класс для сериализации записи дат в JSON'''
		def default(self, o):
			if isinstance(o, datetime):
				return o.isoformat()
			if isinstance(o, bytes):
				return list(o)
			return json.JSONEncoder.default(self, o)

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,                 #CHANGED offset_date=None,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			all_messages.append(message.to_dict())
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	with open('channel_messages.json', 'w', encoding='utf8') as outfile:
		json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main(url):									#changed async def main():
	#changed url = input("Введите ссылку на канал или чат: ")
	channel = await client.get_entity(url)
	await dump_all_messages(channel)
#ezz2
with open('telegram_channels.txt', 'r') as f:
	chats = f.read().splitlines()

import pandas as pd

while True:
	now = abc.datetime.now().date()
	total = pd.DataFrame()
	for chat in chats: #ezz2
		with client:
			client.loop.run_until_complete(main(url=chat))

		#ezz
		with open('channel_messages.json', 'r', encoding='utf-8') as fh:  # открываем файл на чтение
			data = json.load(fh)  # загружаем из файла данные в словарь data
		# print(data[-1], '\n')
		# print(data[-3],'\n')

		id = []
		date = []
		message = []
		for element in data:
			if element['_'] != 'Message':
				continue
			id.append(element['id'])
			date.append(abc.datetime.strptime( \
				element['date'][:10], '%Y-%m-%d').date())
			message.append(element['message'])

		dict = {'id': id, 'date': date, 'message': message}
		#dta = abc.date(year=2020, month=6, day=19) #looooooooooooooooooooooooooooooooooook

		itog = pd.DataFrame(dict)
		itog = itog[itog['date'] >= now]
		#itog.to_csv(str(chat)[5:]+'.csv', sep='|')
		total = pd.concat([itog, total])
	folder_name = str(now)+'Telegram'
	os.mkdir(folder_name)
	total.to_csv(folder_name+'/' + str(now) + 'Telegram.csv', sep='|')
	time.sleep(3600*24)
	#ezz