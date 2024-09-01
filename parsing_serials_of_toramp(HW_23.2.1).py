# Импорт библиотек:
import requests
from bs4 import BeautifulSoup
# Импорт библиотеки записи конечных данных в таблицу:
import pandas as pd

# Импорт данных с внешнего файла:
import initial_data

def list_of_serials_by_score(genre):
    page_num = 1

    # Создаем пустой список, в котором будут храниться записи о сериалах:
    data = []

    while True:
        # Точка входа и с изменяемой внешней переменной
        url = f'https://www.toramp.com/ru/explore/shows/?cpage={page_num}&genre={genre}'
        # Метод Get для получения информации с таблицы сериалов выбранного жанра
        html_content = requests.get(url).text

        soup = BeautifulSoup(html_content, 'lxml') # Начинаем парсинг
        # Поиск всех элементов <div> с классом "content" (контейнеры с сериалами)
        entries = soup.find_all('div', class_='content')

        if len(entries) == 0: # Признак остановки
            break

        for entry in entries:
            # Поиск в каждом элементе <div> элемента <div> с классом "first_line"
            first_line = entry.find('div', class_='first_line')
            # Поиск внутри класса "first_line" элемента <a> и запись значения методом .text:(название сериала)
            serial_name = first_line.find('a').text
            # Внутри first_line поиск элемента <em> и запись значения методом .text:(начало и окончание выхода сериала)
            production_date = first_line.find('em').text

            # В каждом элементе <div> поиск элемент <div> с классом 'score' и запись значения (оценка сериала)
            stats = entry.find('div', class_='stats')
            score = stats.find('div', class_='score').text
            #number_of_votes = stats.find('div', class_='number_of_votes')
            if score is None:
                score = None

            # Записываем все полученные данные о сериалах в виде словаря:
            data.append({'serial name': serial_name, 'production date': production_date, 'score': score})

        page_num += 1  # Переходим на следующую страницу

    return data

# Вывод результатов и запись данных таблицы в файл Excel
serials = list_of_serials_by_score(initial_data.genre)
#print(serials)
print(len(serials))

df = pd.DataFrame(serials)

df.to_excel('serials_rates.xlsx')
