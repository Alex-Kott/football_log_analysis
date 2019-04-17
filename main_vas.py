from collections import defaultdict, OrderedDict
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random


def get_color():
    r = lambda: random.randint(0, 255)

    return '#%02X%02X%02X' % (r(), r(), r())


df = pd.read_csv('football', sep='\t')

rates = defaultdict(lambda: defaultdict(int))
words = ['чм', 'чемпионат', 'футбол', 'счёт', 'счет', 'матч', 'трансляция', 'сборная']

for i, row in df.iterrows():
    print(i, flush=True, end='\r')

    query = row['normal_query']
    query_dt = str(datetime.fromisoformat(row['datetime']).date())

    for word in words:
        if not isinstance(query, str):
            continue
        if query.find(word) != -1:
            rates[word][query_dt] += 1

plt.rcParams['figure.figsize'] = (15, 10)
subplot = plt.subplot()

handles = []

for word, v in rates.items():
    ordered_dict = OrderedDict()
    for i in sorted(v.keys()):
        ordered_dict[i] = v[i]

    axis_x = ordered_dict.keys()
    axis_y = ordered_dict.values()

    color = get_color()
    subplot.plot(axis_x, axis_y, c=color)
    patch = mpatches.Patch(color=color, label=word)
    handles.append(patch)

plt.legend(handles=handles)

plt.xlabel("Запросы")
plt.ylabel("Время")
plt.title("Слова")

plt.savefig('pic_vas.png')
plt.clf()


