import sys

class AutoParser:
    def __init__(self, dictionary, company_name):
        """
        Универсальный класс для парсинга любых компаний

        Методы:
            self._find_company_dfs_csv - находит все упоминания компании в директории
            self._combine_dfs          - комбинирует датафреймы, найденные в директории, либо переданные в качестве
                 аргумента
            self.fit_transform         - выполняет основную последовательность операций
        """
        self.link = None
        self.current_page = None
        self.dictionary = dictionary
        self.company_name = company_name #CHANGED
        self.last_page = self._get_last()

    def _get_last(self):
        self.link = self.dictionary[self.company_name]
        soup = self._go_to(self.dictionary[self.company_name])
        return int(soup.find_all('div', 'mfd-paginator')[0].contents[-2].text)

    def _go_to(self, url):
        import sys
        from bs4 import BeautifulSoup
        from urllib.request import urlopen

        html_doc = urlopen(url).read()
        soup = BeautifulSoup(html_doc, features='html.parser')
        return soup

    def _likes_finder(self, post):
        likes = post.find('span', 'u')
        if likes is None:
            likes = 0
        else:
            likes = likes.text
        return likes

    def run(self):
        import time
        import json
        import pandas as pd
        from tqdm import tqdm

        all_data = {}
        counter = 0

        # ищет уже спаршенные данные в директории
        try:
            with open('text/{}_param.txt'.format(self.company_name), 'r') as f:
                page_num = json.loads(f.readline())['param']
        except:
            page_num = 0

        if self.current_page is not None:
            page_num = self.current_page
        print('Изначальное состояние: n = {}'.format(page_num + 1))

        for page_numer in tqdm(range(page_num, self.last_page + 1)):
            try:
                # ссылка на компанию тоже нужно поменять
                base_url = '{}&page={}'.format(self.link, page_numer)
                soup = self._go_to(base_url)
                posts = soup.find_all('div', 'mfd-post')
                for post in posts:
                    user_rate = post.find('div', 'mfd-poster-info-rating mfd-icon-profile-star')
                    if user_rate is None:
                        user_rate = 0
                    else:
                        user_rate = user_rate.text
                    times = post.find('div', 'mfd-post-top-1').text
                    if post.find_all('div', 'mfd-quote-text') != []:
                        text = post.find_all('div', 'mfd-quote-text')[-1].text
                    else:
                        text = 'DELETED'
                    likes = self._likes_finder(post)

                    counter += 1
                    all_data.update({counter: {
                        'user_rate': user_rate,
                        'time': times,
                        'likes': likes,
                        'text': text
                    }})
                time.sleep(2)  # задержка на промежутки парсинга

                if page_numer % 1 == 0:
                    pd.DataFrame(all_data).T.to_csv('{}_{}.csv'.format(self.company_name, page_numer), sep='|')
                    DfMerger(self.company_name).fit_transform()
                    dictionary = {'param': page_numer}
                    with open('{}_param.txt'.format(self.company_name), 'w') as f:
                        json.dump(dictionary, f)

            except:
                dictionary = {'param': page_numer}
                print('\nПарсинг приостановлен, номер итерации: {}'.format(page_numer))
                with open('{}_param.txt'.format(self.company_name), 'w') as f:
                    json.dump(dictionary, f)
                print('Параметры сохранены, можете зыкрывать приложение!')
                time.sleep(10)
        print('Сохраняюсь')
        # меняешь компанию - измени название сохраняемого файла
        pd.DataFrame(all_data).T.to_csv('{}_{}.csv'.format(self.company_name, page_num), sep='|')
        DfMerger(self.company_name).fit_transform()
        return 'Парсинг завершен!'



class DfMerger:
    def __init__(self, company_name, dfs=None):
        """
        Класс наследует instance объекта Parser, чтобы использовать все его переменные

        Методы:
            self._find_company_dfs_csv - находит все упоминания компании в директории
            self._combine_dfs          - комбинирует датафреймы, найденные в директории, либо переданные в качестве
                 аргумента
            self.fit_transform         - выполняет основную последовательность операций
        """
        self.company_name = company_name
        self.dfs_to_merge = dfs

    def _find_company_dfs_csv(self):
        import os

        company_name_files = [i for i in os.listdir() if len(i.split(self.company_name)) != 1]
        return [i for i in company_name_files if len(i.split('.csv')) != 1]

    def _combine_dfs(self, all_company_names_list, mode=0, sep='|'):
        import pandas as pd
        import os

        if mode == 0:
            full_df = pd.DataFrame()

            # Мержим каждый датафрейм из списка
            for file in all_company_names_list:
                df = pd.read_csv(file, sep=sep, index_col=0)
                full_df = full_df.append(df).reset_index(drop=True).drop_duplicates().reset_index(drop=True)

            name_to_save = '{}_parsed.csv'.format(self.company_name)
            full_df.to_csv(name_to_save, sep=sep)

            # Удаляем временные файлы
            for file in all_company_names_list:
                if file != name_to_save:
                    os.remove(file)
        else:

            # Мержим датафреймы из списка датафреймов
            full_df = pd.DataFrame()
            for df in all_company_names_list:
                full_df = full_df.append(df).reset_index(drop=True).drop_duplicates()
            return full_df

    def fit_transform(self):
        """
        Функция мержит несколько датафреймов удаляя дубликаты, сбрасывая индексы
        """
        if self.dfs_to_merge is None:
            return self._combine_dfs(self._find_company_dfs_csv(), mode=0)
        else:
            return self._combine_dfs(self.dfs_to_merge, mode=1)


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

sys.setrecursionlimit(999999999)
#parser = Parser(dictionary).run()
"""
#Определяем последнюю страницу на сейчас, чтобы знать откуда парсить

import json
for index, company in enumerate(dictionary):
    if index in [0,21,42]:
        continue
    page_numer = AutoParser(dictionary, company).last_page
    dict = {'param': page_numer}
    with open('{}_param.txt'.format(company), 'w') as f:
        json.dump(dict, f)     


#Парсим
for index, company in enumerate(dictionary):
    if index in [0,21,42]:
        continue
    parser = AutoParser(dictionary, company).run()
"""
if __name__ == '__main__':
    import time
    import json
    import datetime
    import os
    already_parsed = False
    previous_datetime = datetime.datetime(2020, 6, 30, hour = 2, minute=28) #Заглушка
    while True:
        now = datetime.datetime.now()
        if now.isoweekday() != previous_datetime.isoweekday():
            already_parsed = False
            previous_datetime = datetime.datetime.now()
        if already_parsed:
            time.sleep(3600)
            continue
        if now.isoweekday() in [7,1]: #По выходным не парсим, а лишь меняем страницы. А так как мы парсим утром следующего дня, то парсинг съехал с (сб, вс) на (вс,пн)
            for index, company in enumerate(dictionary):
                if index in [0, 21, 42]:
                    continue
                page_numer = AutoParser(dictionary, company).last_page
                dict = {'param': page_numer}
                with open('{}_param.txt'.format(company), 'w') as f:
                    json.dump(dict, f)

            already_parsed = True
            time.sleep(3600)

        else:
            for index, company in enumerate(dictionary):
                if index in [0, 21, 42]:
                    continue
                parser = AutoParser(dictionary, company).run()

            folder_name = str(now.date())
            os.mkdir(folder_name)
            files = os.listdir()
            for file in files:
                if str(file)[-3:] == 'csv':
                    os.replace(file, folder_name + '/' + file)

            already_parsed = True
            time.sleep(3600)
