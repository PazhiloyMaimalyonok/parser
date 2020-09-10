import pickle
from datetime import datetime, timedelta
import emoji
SMILES = ['✅', '❎']

def soobschenye(last_buy_date, last_sell_date):
       with open("/home/danyanyam/flask/Библиотека/data/pickles/sell_orders.pickle", "rb") as fobj:
              sell =  pickle.load(fobj)
       with open("/home/danyanyam/flask/Библиотека/data/pickles/buy_orders.pickle", "rb") as fobj:
              buy = pickle.load(fobj)
       with open("/home/danyanyam/flask/Библиотека/data/pickles/portfel.pickle", "rb") as fobj:
              data = pickle.load(fobj)

       result = []
       if datetime.now().isoweekday() in [6, 7]:
              return False
       if datetime.now().isoweekday() in [1,2,3,4,5]:
              if (sell['date'] != last_sell_date) and (buy['date'] != last_buy_date):
                     last_buy_date, last_sell_date = buy['date'], sell['date']

              else:
                     return False

       date = datetime.now().date()
       buy = buy['orders']
       sell = sell['orders']
       last_update_of_portfolio, amount_of_deals_this_month, cumulated_yield, mean_yield, volatility, musor = data['current_conditions'][0].values()

       if buy != []:
              #print(f'Покупки на {date}:', *buy)
              zatychka = ''
              for el in buy:
                     zatychka += el + ', '
              zatychka = str(zatychka)[:-2]
              result.append(str(f'{SMILES[0]}Покупки на {date}: ') + zatychka + '\n')
       else:
              #print(f'На дату {date} покупок акций не запланировано')
              result.append(str(f'На дату {date} покупок акций не запланировано') + '\n')

       if list(sell)!= []:
              #print("Продажи", *sell)
              for el in sell:
                     zatychka += el + ', '
              zatychka = str(zatychka)[:-2]
              result.append('{SMILES[1}Продажи' + zatychka + '\n')
       else:
              #print('Ничего не продаем')
              result.append('Ничего не продаем' + '\n')
       #print(f'Характеристика портфеля: Совокупная доходность = {yelda}, количество сделок за месяц = {amount}, волатильность = {vol}, средняя доходность = {mean_yelda}')
       result.append(f'Характеристика портфеля: Совокупная доходность = {cumulated_yield * 100} %, количество сделок за месяц = {amount_of_deals_this_month}, волатильность = {volatility* 100}%')

       return result, last_buy_date, last_sell_date
#a = soobschenye()
#print(*a, sep='\n')
