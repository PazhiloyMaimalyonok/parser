import numpy as np
import pandas as pd
import os

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import csv

dictionary = {
            '#----------# ДВАДЦАТЬ НАИБОЛЬШИХ #----------#': '#----------#',
            'alrosa': r'http://forum.mfd.ru/forum/thread/?id=4313',
            'aeroflot': r'http://forum.mfd.ru/forum/thread/?id=61912',
            'fees': r'http://forum.mfd.ru/forum/thread/?id=61148',
            'gazprom': r'http://forum.mfd.ru/forum/thread/?id=61478',
            'gtl': r'http://forum.mfd.ru/forum/thread/?id=66603',
            'lukoil': r'http://forum.mfd.ru/forum/thread/?id=62203',
            'mmk': r'http://forum.mfd.ru/forum/thread/?id=63263',
            'mts': r'http://forum.mfd.ru/forum/thread/?id=63940',
            'moex': r'http://forum.mfd.ru/forum/thread/?id=66517',
            'magnit': r'http://forum.mfd.ru/forum/thread/?id=61993',
            'novatek': r'http://forum.mfd.ru/forum/thread/?id=62709',
            'nlmk': r'http://forum.mfd.ru/forum/thread/?id=64032',
            'nornikel': r'http://forum.mfd.ru/forum/thread/?id=26106',
            'polyus': r'http://forum.mfd.ru/forum/thread/?id=60251',
            'rosneft': r'http://forum.mfd.ru/forum/thread/?id=61941',
            'surgutneftegas': r'http://forum.mfd.ru/forum/thread/?id=30060',
            'sberbank': r'http://forum.mfd.ru/forum/thread/?id=62075',
            'severstal': r'http://forum.mfd.ru/forum/thread/?id=62342',
            'vtb': r'http://forum.mfd.ru/forum/thread/?id=45229',
            'yandex': r'http://forum.mfd.ru/forum/thread/?id=68203',
            '#----------# ДВАДЦАТЬ СРЕДНИХ #----------#': '#----------#',
            'afk sistema': r'http://forum.mfd.ru/forum/thread/?id=62206',
            'akron': r'http://forum.mfd.ru/forum/thread/?id=62599',
            'fosagro': r'http://forum.mfd.ru/forum/thread/?id=64267',
            'gazpromneft': r'http://forum.mfd.ru/forum/thread/?id=62100',
            'lenta': r'http://forum.mfd.ru/forum/thread/?id=68291',
            'lsr': r'http://forum.mfd.ru/forum/thread/?id=62144',
            'mechel': r'http://forum.mfd.ru/forum/thread/?id=61771',
            'mosenergo': r'http://forum.mfd.ru/forum/thread/?id=61698',
            'NMTP': r'http://forum.mfd.ru/forum/thread/?id=62058',
            'PIK': r'http://forum.mfd.ru/forum/thread/?id=61161',
            'raspadskaya': r'http://forum.mfd.ru/forum/thread/?id=62771',
            'rostelekom': r'http://forum.mfd.ru/forum/thread/?id=82263',
            'rosseti': r'http://forum.mfd.ru/forum/thread/?id=62235',
            'rusgidro': r'http://forum.mfd.ru/forum/thread/?id=60669',
            'rusal': r'http://forum.mfd.ru/forum/thread/?id=63559',
            'TMK': r'http://forum.mfd.ru/forum/thread/?id=63060',
            'TGK-1': r'http://forum.mfd.ru/forum/thread/?id=61217',
            'transneft': r'http://forum.mfd.ru/forum/thread/?id=61526',
            'uralkaliy': r'http://forum.mfd.ru/forum/thread/?id=60730',
            'unipro': r'http://forum.mfd.ru/forum/thread/?id=63830',
            '#----------# ДВАДЦАТЬ МАЛЫХ #----------#': '#----------#',
            'ashinskiy_metzavod': r'http://forum.mfd.ru/forum/thread/?id=61592',
            'apteki_36_6': r'http://forum.mfd.ru/forum/thread/?id=61569',
            'arsagera': r'http://forum.mfd.ru/forum/thread/?id=60997',
            'cherkizovo': r'http://forum.mfd.ru/forum/thread/?id=61943',
            'CHZPSN': r'http://forum.mfd.ru/forum/thread/?id=66106',
            'dagsbyt': r'http://forum.mfd.ru/forum/thread/?id=62621',
            'GAZ': r'http://forum.mfd.ru/forum/thread/?id=64839',
            'GTL': r'http://forum.mfd.ru/forum/thread/?id=66603',
            'irkut': r'http://forum.mfd.ru/forum/thread/?id=61926',
            'KTK': r'http://forum.mfd.ru/forum/thread/?id=62767',
            'lenergo': r'http://forum.mfd.ru/forum/thread/?id=63912',
            'NKNH': r'http://forum.mfd.ru/forum/thread/?id=62842',
            'rusolovo': r'http://forum.mfd.ru/forum/thread/?id=67295',
            'rollman': r'http://forum.mfd.ru/forum/thread/?id=66335',
            'sib_gostinets': r'http://forum.mfd.ru/forum/thread/?id=70539',
            'sollers': r'http://forum.mfd.ru/forum/thread/?id=61394',
            'saratovskiy_npz': r'http://forum.mfd.ru/forum/thread/?id=64855',
            'seligdar': r'http://forum.mfd.ru/forum/thread/?id=64669',
            'tantal': r'http://forum.mfd.ru/forum/thread/?id=65404',
            'YATEK': r'http://forum.mfd.ru/forum/thread/?id=65074'
        }


def post_dt_parse(post_dt, cur_dt, time_for_old_posts='00:00'):
    '''
    function parse datetime from tinkoff post to separate date and time format
    !!!don't check posts inserted years ago!!!
    params
    =====================
        post_dt - string with inserted post datetime in forum format
        cur_dt - datetime, current datetime, to calc diff
        time_for_old_posts - time format for posts inserted 2 and more days ago
    return
    =====================
        [string of date, string of time]
        string of date - %Y-%m-%d (for posts during current month)
                         %Y-%m (for posts month ago or later).
        string of time - %H:%M (for minutes ago or yesterday posts)
                         %H:00 (for today hours ago posts),
                         time_for_old_posts - for older posts

        if no parsing entries, return ['ERROR', post_dt]

    '''
    # массивы для сопоставления
    today_min_array = ['минуту назад', 'минут назад', 'минуты назад']
    today_one_hour = ['час назад']
    today_hour_array = ['1 час назад', 'часов назад', 'часа назад']
    yestd_array = ['Вчера']
    day_array = ['день назад', 'дней назад', 'дня назад']
    one_month_array = ['месяц назад']
    month_array = ['месяцев назад', 'месяца назад']
    # парсим минуты назад (пример '9 минут назад')
    if any(s in post_dt for s in today_min_array):
        delta = int(post_dt.split()[0])
        return ((cur_dt - timedelta(minutes=delta)).strftime("%Y-%m-%d %H:%M").split())

    # парсим час назад (пример 'час назад')
    if any(s in post_dt for s in today_one_hour):
        delta = 1
        return ((cur_dt - timedelta(hours=delta)).strftime("%Y-%m-%d %H:00").split())

        # парсим часы назад (пример '1 час назад')
    if any(s in post_dt for s in today_hour_array):
        delta = int(post_dt.split()[0])
        return ((cur_dt - timedelta(hours=delta)).strftime("%Y-%m-%d %H:00").split())

    # парсим вчера (пример 'Вчера в 12:38)
    if any(s in post_dt for s in yestd_array):
        return ([(cur_dt - timedelta(days=1)).strftime("%Y-%m-%d"), post_dt.split()[2]])

    # парсим дни назад (пример '2 дня назад')
    if any(s in post_dt for s in day_array):
        delta = int(post_dt.split()[0])
        return ([(cur_dt - timedelta(days=delta)).strftime("%Y-%m-%d"), time_for_old_posts])

    # парсим месяц назад (пример 'месяц назад')
    if any(s in post_dt for s in one_month_array):
        delta = 1
        return ([(cur_dt + relativedelta(months=-delta)).strftime("%Y-%m"), time_for_old_posts])

    # парсим месяцы назад (пример '2 месяца назад')
    if any(s in post_dt for s in month_array):
        delta = int(post_dt.split()[0])
        return ([(cur_dt + relativedelta(months=-delta)).strftime("%Y-%m"), time_for_old_posts])

    else:
        return (['ERROR', post_dt])


def post_parsing(post, cur_dt):
    '''
    parse post into strings
    params
    =====================
    post = WebElement
    cur_dt = datetime, current date

    returns
    =====================
    [post_date, post_time, author, message, likes count, comments count]
     post_date, post_time - date and time of inserted post (see function post_dt_parse for detail)

    ERROR - if no element found during parsing
    '''

    # Дата вставки поста ( от текущей)
    try:
        post_dt = post.find_element_by_class_name('PulsePostAuthor__inserted_3x9yu').text
        post_date, post_time = post_dt_parse(post_dt, cur_dt)
    # если не находим текущий класс
    except NoSuchElementException:
        post_date, post_time = 'ERROR', 'ERROR'

    # Автор
    try:
        author = post.find_element_by_class_name('PulsePostAuthor__nicknameLink_19Aca').text
    except NoSuchElementException:
        author = 'ERROR'

    # Текст сообщения
    # по умолчанию, ставится в начале текста тикер как гипер ссылка на график. я его оставляю
    try:
        message = post.find_element_by_class_name('PulsePostCollapsed__text_1ypMP').text
        # меняем текст в строку (убираем символ начала новой строки)
        message = message.replace('\n', ' ')
    except NoSuchElementException:
        message = 'ERROR'

    # кол-во лайков
    # строку вида "1 нравится", разделяем и берем первый элемент
    try:
        likes = post.find_element_by_class_name('PulsePostBody__likes_3qcu0').text.split()[0]
    except NoSuchElementException:
        likes = 'ERROR'

    # данный блок присутствует в контейнере поста только после того, как появляются комментарии
    # если блока нет - значит комментариев нет
    # в остальном парсим оп аналогии с лайками
    # потенциально пропущена проверка в целом на правильность парсинга комментариев, что класс не поменялся
    try:
        comments = post.find_element_by_class_name('PulsePost__commentLink_3J9Ff').text.split()[0]
    except NoSuchElementException:
        comments = 0

    return [post_date, post_time, author, message, likes, comments]


def ticker_parsing(ticker, output_dir='', webdriver_path=''):
    '''
    parse one ticker from tinkoff forum and save to csv
    use Chrome webdriver

    params
    =====================
    ticker - stock symbol
    output_dir - dir to save csv, save in execution path by default
    webdriver_path - path to chrome webdirver, use executio path by default

    return
    =====================
    parsing result, string
    '''
    # определим путь к бумаге на сайте тинькова
    url = 'https://www.tinkoff.ru/invest/stocks/%s/pulse/' % ticker

    # инициализируем драйвер и обращаемся с страничке
    if webdriver_path == '':
        browser = webdriver.Chrome()
    else:
        browser = webdriver.Chrome(webdriver_path)

    browser.get(url)
    # блок для скролла
    block = browser.find_element_by_tag_name("body")

    # определим текущую дату скачивания
    cur_dt = datetime.today()
    # переменные для проверки, достигли мы конца списка или нет
    new_page_height = 0
    old_page_height = 0
    # счетчик и предел одинаковых значенй
    counter = 0
    limit = 20
    counter2 = 0  # CHANGED
    # начинаем скроллить, пока не достигним конца списка
    while True:
        # Scroll down to bottom
        block.send_keys(Keys.PAGE_DOWN)
        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight-  1.8 * %i);" %h)

        # важно! иногда не успевает страница отработать и в итоге не все данные загрузяться
        time.sleep(0.8)
        new_page_height = browser.execute_script("return document.body.scrollHeight")
        # Если значение не изменилось, увеличиваем счетчик одинаковых значений
        # иначе обнуляем счетчик
        if new_page_height == old_page_height:
            counter += 1
        else:
            counter = 0
        # если достигли лимита повторов, выходим из цикла
        if counter == limit:
            break;
        # old_page_height = new_page_height
        # """
        counter2 += 1  # CHANGED
        if counter2 % 10 == 0:
            posts = block.find_elements_by_class_name('PulsePost__container_1cDSs')
            post_count = len(posts)
            posts_texts = []
            for i in range(post_count):
                posts_texts.append(post_parsing(posts[i], cur_dt))
            df = pd.DataFrame(posts_texts)
            df.columns = ['date', 'time', 'author', 'message', 'likes', 'comments']
            for date in np.unique(df.date.values):
                try:
                    date = datetime.strptime(date, "%Y-%m-%d").date()
                    if date != cur_dt.date():
                        browser.quit()
                        if len(posts_texts) == 0:
                            return 'ticker : ' + ticker + '; No posts parsing!!!'
                        df['date'] = [datetime.strptime(x, "%Y-%m-%d").date() for x in df.date.values]
                        df = df[df.date == cur_dt.date()]
                        df.to_csv(output_dir + ticker + '.csv', index=False, header=True)
                        return 'Успех'
                except:
                    print(date)
        # """
        old_page_height = new_page_height
        # print(browser.execute_script("return document.body.scrollHeight"), end = '\r')

    # все контейнеры с постами
    posts = block.find_elements_by_class_name('PulsePost__container_1cDSs')
    post_count = len(posts)

    # парсим посты и записываем их в массив
    posts_texts = []
    for i in range(post_count):
        posts_texts.append(post_parsing(posts[i], cur_dt))

        # проверяем, если нет постов, то выходим
    if len(posts_texts) == 0:
        browser.quit()
        return 'ticker : ' + ticker + '; No posts parsing!!!'

    # записываем в csv
    df = pd.DataFrame(posts_texts)
    df.columns = ['date', 'time', 'author', 'message', 'likes', 'comments']
    # может быть стоит явно указать кодировку
    df.to_csv(output_dir + ticker + '.csv', index=False, header=True)

    # закрываем браузер и выходим
    browser.quit()
    return 'ticker : ' + ticker + '; earliest date : ' + posts_texts[-1][0] + '; posts count : ' + str(post_count)

#ticker_parsing('AFLT', 'C:/Users/79126/Desktop/project/Auto_parser/Pulse_Parser/', 'C:/Users/79126/Downloads/chromedriver_win32/chromedriver.exe')
with open('tickers.txt', 'r') as f:
    tickers = f.read().splitlines()
not_parsed = []
now = datetime.now()
folder_name = str(now.date())
os.mkdir(folder_name)
for index, ticker in enumerate(tickers[0:10]):
    if index==2:
        break
    try:
        ticker_parsing(ticker, str(folder_name) + '/', 'C:/Users/79126/Downloads/chromedriver_win32/chromedriver.exe')
    except:
        not_parsed.append(ticker)
        print(f'Не получилось спарсить: {ticker}')
