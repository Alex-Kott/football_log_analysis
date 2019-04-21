from collections import defaultdict, OrderedDict
from datetime import datetime
from typing import Dict

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random


def get_rand_color() -> str:
    r = lambda: random.randint(0, 255)

    return '#%02X%02X%02X' % (r(), r(), r())


def make_grapgh(rates: Dict) -> None:
    plt.rcParams['figure.figsize'] = (35, 20)  # создаём заготовку
    subplot = plt.subplot()

    handles = []  # список обработчиков

    for theme, v in rates.items():  # для каждой темы отдельный график
        ordered_dict = OrderedDict()

        for i in sorted(v.keys()):  # сортировка по дате
            ordered_dict[i] = v[i]

        axis_x = ordered_dict.keys()  # значения для осей X и Y
        axis_y = ordered_dict.values()

        color = get_rand_color()  # берём случайный цвет для каждой темы
        subplot.plot(axis_x, axis_y, c=color)
        patch = mpatches.Patch(color=color, label='; '.join(theme))
        handles.append(patch)

    plt.legend(handles=handles)  # делаем легенду графика

    plt.xlabel("Theme requests")
    plt.ylabel("Dates")
    plt.title("Requests")

    plt.savefig('pic.png')


def main(log_file_name: str) -> None:
    df = pd.read_csv(log_file_name, sep='\t')  # читаем логи в датафрейм, использую в качестве разделителя знак табуляции

    score = defaultdict(lambda: defaultdict(int))  # создаём словарь для рейтинга
    themes = [  # naive implementation
        ('чм', 'чемпионат', 'счёт', 'счет', 'результат', 'трансляция', 'матч', 'футбол', 'сборная'),
        ('хостел', 'отель', 'гостиница', 'снять жильё', 'снять квартиру', 'ставки', 'букмекерская', 'букмекер')
        ]

    for i, row in df.iterrows():  # итерируемся по логам
        print(i, flush=True, end='\r')
        query = row['normal_query']
        query_dt = str(datetime.fromisoformat(row['datetime']).date())

        for theme in themes:
            for theme_word in theme:
                if not isinstance(query, str):
                    continue
                if query.find(theme_word) != -1:
                    score[theme][query_dt] += 1  # если хоть одно слово из темы находится в запросе -- увеличиваем рейтинг
    make_grapgh(score)  # строим график по полученным результатам


if __name__ == "__main__":
    main('log')  # вызываем основную функцию, передаём имя файла с логами
