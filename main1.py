import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import urllib.parse as url_parser
from collections import defaultdict


def search_words(text, words):
    for word in words:
        if text.find(word) != -1:
            return True
    return False


def count_video_related(total, video_related_requests):
    names = ['Requests about TV', 'Another requests']
    values = [video_related_requests, total]

    dpi = 80

    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 12})

    plt.title('Request about TV (%)')

    xs = range(len(names))

    plt.pie(
        values,
        autopct='%.1f',
        radius=1.1,
        explode=[0.15] + [0 for _ in range(len(names) - 1)],
        colors=['red', 'green'],
        shadow=True,
        counterclock=False)
    plt.legend(
        bbox_to_anchor=(-0.16, 0, 0, 0.25),
        loc='lower left',
        labels=names)
    fig.savefig('img1.png')


def count_by_device(touch, desktop):
    names = ['Mobile devices', 'Desktop']
    values = [touch, desktop]

    dpi = 80

    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})

    plt.title('Desktop/mobile devices relation')

    xs = range(len(names))

    plt.pie(
        values,
        autopct='%.1f',
        radius=1.1,
        explode=[0.15] + [0 for _ in range(len(names) - 1)],
        colors=['red', 'green'],
        shadow=True,
        counterclock=False)
    plt.legend(
        bbox_to_anchor=(-0.16, 0, 0, 0.25),
        loc='lower left',
        labels=names)
    fig.savefig('img2.png')


if __name__ == "__main__":

    log = pd.read_csv("log", sep='\t', header=0)

    devices = defaultdict(int)
    count = 0
    total = len(log)
    for index, row in log.iterrows():
        print(f"{index}/{total}", flush=True, end='\r')

        # print(index, row)

        text = row['normal_query']


        # continue
        # query = url_parser.urlparse(row['request']).query
        # try:
        #     text = url_parser.parse_qs(query).get('text')[0]
        # except TypeError:
        #     continue

        video_content_search = []
        filter_lexems = [' телев', 'телепер', 'телепрог', 'смотреть', 'сериал', 'кино', 'сезон']
        try:
            if search_words(text, filter_lexems):
                count = count + 1
                # if count > 10000:
                # break
                video_content_search.append(text)
                # devices[row['device']] += 1
        except Exception as e:
            print(e)

    count_video_related(count, index)
    # count_by_device(devices["touch"], devices["desktop"])




