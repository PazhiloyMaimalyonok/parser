import json
import datetime
import pandas as pd
with open('channel_messages.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
    data = json.load(fh) #загружаем из файла данные в словарь data
print(data[-1],'\n')
#print(data[-3],'\n')

id = []
date = []
message = []
for element in data:
    if element['_'] != 'Message':
        continue
    id.append(element['id'])
    date.append(datetime.datetime.strptime(\
        element['date'][:10], '%Y-%m-%d').date())
    message.append(element['message'])

dict = {'id': id, 'date': date, 'message': message}
#now = datetime.datetime.now().date()
dta = datetime.date(year=2020, month = 6, day = 21)

itog = pd.DataFrame(dict)
itog = itog[itog['date']>=dta]
#itog.to_csv('.csv', sep='|')