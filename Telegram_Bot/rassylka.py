import pickle
from datetime import datetime, timedelta

def soobschenye():
       with open("/home/danyanyam/flask/Библиотека/data/pickles/portfel.pickle", "rb") as fobj:
              data =  pickle.load(fobj)
       result = []
       counter = 0
       if datetime.now().isoweekday() in [6, 7]:
              return False
       if datetime.now().isoweekday() == 1:
              required_date = (datetime.now().date() - timedelta(days = 2)).strftime("%d.%m.%Y")[:8]
       else:
              required_date = datetime.now().date().strftime("%d.%m.%Y")[:8]
       for x in data['historical_performance']:
              if x['date_of_operation'] == None:
                     continue
              if str(x['date_of_operation'])[:8] == required_date:
                     #print(x)
                     info = x
                     counter +=1
       if counter == 0:
              return [f'Файла с данными за сегодня {datetime.now().date()} нет']
       date = datetime.now().date()
       buy = list(info['orders']['buy'].keys())
       sell = list(info['orders']['sell'].keys())
       a, pr, yelda, amount, vol, mean_yelda, hold, perf = data.values()
       if buy != []:
              #print(f'Покупки на {date}:', *buy)
              zatychka = ''
              for el in buy:
                     zatychka += el + ', '
              zatychka = str(zatychka)[:-2]
              result.append(str(f'Покупки на {date}: ') + zatychka + '\n')
       else:
              #print(f'На дату {date} покупок акций не запланировано')
              result.append(str(f'На дату {date} покупок акций не запланировано') + '\n')

       if list(sell)!= []:
              #print("Продажи", *sell)
              for el in sell:
                     zatychka += el + ', '
              zatychka = str(zatychka)[:-2]
              result.append('Продажи' + zatychka + '\n')
       else:
              #print('Ничего не продаем')
              result.append('Ничего не продаем' + '\n')
       #print(f'Характеристика портфеля: Совокупная доходность = {yelda}, количество сделок за месяц = {amount}, волатильность = {vol}, средняя доходность = {mean_yelda}')
       result.append(f'Характеристика портфеля: Совокупная доходность = {yelda}, количество сделок за месяц = {amount}, волатильность = {vol}, средняя доходность = {mean_yelda}')
       return result
#a = soobschenye()
#print(*a, sep='\n')
