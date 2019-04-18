from collections import defaultdict, OrderedDict
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random


def get_color():
    r = lambda: random.randint(0, 255)

    return '#%02X%02X%02X' % (r(), r(), r())


#  программа начинает исполняться тут
df = pd.read_csv('football', sep='\t')  # читаем файл логов в датафрейм. Преимущество датафрейма --
                                # он оптимизирован для работы с табличными данными. Можно было бы и просто в список считать, но так удобнее

rates = defaultdict(lambda: defaultdict(int))  # создаём словарь для хранения метрик
words = ['чм', 'чемпионат', 'футбол', 'счёт', 'счет', 'матч', 'трансляция', 'сборная']  # слова, наличие которых будем искать

for i, row in df.iterrows():  # итерируемся логам, i - номер строки, row - сама строка
    print(i, flush=True, end='\r')  # пишем в консоль номер строки

    query = row['normal_query']  # содержимое файла в датафрейме преобразовано к таблице из двух колонок: первая -- normal_query, вторая -- дата и время запроса
    query_dt = str(datetime.fromisoformat(row['datetime']).date())  # преобразуем дату к строке, это будет наш индекс в словаре рейтингов

    for word in words:  # ищем каждое слово из списка в строке. Если находим -- увеличиваем счётчик на 1
        if not isinstance(query, str):
            continue
        if query.find(word) != -1:
            rates[word][query_dt] += 1

plt.rcParams['figure.figsize'] = (15, 10)  # строим график для отображения результатов. Здесь задаётся размер.
subplot = plt.subplot()

handles = []

for word, v in rates.items():
    ordered_dict = OrderedDict()
    for i in sorted(v.keys()): # сортируем по дате
        ordered_dict[i] = v[i]

    axis_x = ordered_dict.keys()  # задаём значения по осям
    axis_y = ordered_dict.values()

    color = get_color()  # получаем случайный цвет для каждого графика
    subplot.plot(axis_x, axis_y, c=color)
    patch = mpatches.Patch(color=color, label=word)
    handles.append(patch)

plt.legend(handles=handles)  # создаём легенду графика (подписи)

plt.xlabel("Запросы")
plt.ylabel("Время")
plt.title("Слова")

plt.savefig('pic_vas.png')  # сохраняем в файл
plt.clf()


