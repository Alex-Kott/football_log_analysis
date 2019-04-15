from collections import defaultdict, OrderedDict
from datetime import datetime
from functools import lru_cache
from random import randint

import pandas as pd
import pymorphy2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random


def get_rand_color():
    r = lambda: random.randint(0, 255)

    return '#%02X%02X%02X' % (r(), r(), r())


@lru_cache(maxsize=999999)
def normalize(query):
    words = query.split(' ')
    morph = pymorphy2.MorphAnalyzer()

    return [morph.parse(word)[0].normal_form for word in words]


def draw_graph(rates):

    plt.rcParams['figure.figsize'] = (35, 20)
    subplot = plt.subplot()

    handles = []

    for theme, v in rates.items():
        ordered_dict = OrderedDict()
        # print(theme)
        # for query_dt, queries_per_date in v.items():
            # print(query_dt, queries_per_date)
            # dates.add(query_dt)

        for i in sorted(v.keys()):
            ordered_dict[i] = v[i]

        # axis_x = list(v.keys())
        # axis_y = list(v.values())

        axis_x = ordered_dict.keys()
        axis_y = ordered_dict.values()

        # print('                ', ' '.join(theme), axis_x, axis_y, flush=True, end='\r')
        color = get_rand_color()
        subplot.plot(axis_x, axis_y, c=color)
        patch = mpatches.Patch(color=color, label=' '.join(theme))
        handles.append(patch)

    plt.legend(handles=handles)

    plt.xlabel("Количество запросов по теме")
    plt.ylabel("Время")
    plt.title("Поисковые запросы")

    # plt.axvline(x='2018-06-14', linestyle=':', color='grey')
    # plt.axvline(x='2018-07-15', linestyle=':', color='grey')

    plt.savefig('pic.png')
    plt.clf()
    # plt.show()



def main():
    df = pd.read_csv('log', sep='\t')

    rates = defaultdict(lambda: defaultdict(int))
    themes = [  # naive implementation
        ('чм', 'чемпионат'),
        ('хостел', 'отель', 'гостиница'),
        ('счёт', 'счет'),
        ('ставки', 'букмеркер', 'букмекерская'),
        ('трансляция', ),
        ('футбол',),
        ]

    for i, row in df.iterrows():
        print(i, flush=True, end='\r')

        query = row['normal_query']
        query_dt = str(datetime.fromisoformat(row['datetime']).date())

        normal_words = normalize(query)

        for theme in themes:
            if (set(theme) & set(normal_words)) != set():
                # print(normal_words, theme)
                # if rates.get(theme):
                #     rates[theme] = defaultdict(int)

                rates[theme][query_dt] += 1
                draw_graph(rates)
                # break

        # for theme, rate in rates.items():
        #     print(theme)
        #     for dt, ones in rate.items():
        #         print(dt, ones)
        #     print('\n')
        #
        # print('________________________________________________________')


        # if i == 1000:
        #     break



def f():
    return {randint(0, 100): randint(0, 100) for i in range(100)}


if __name__ == "__main__":
    main()



    d = {
        ('a', 'b'): {

        },


        # {
        #     1: 13,
        #     2: 43,
        #     5: 23,
        #     3: 12
        # }
    }

    d = {(f'{i}',): f() for i in range(1)}
    # draw_graph(d)