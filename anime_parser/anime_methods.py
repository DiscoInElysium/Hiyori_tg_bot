import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date

import re


def anime_stats(title_url):
    result = requests.get(url=title_url)
    soup = BeautifulSoup(result.text, 'lxml')

    test = soup.find("dl", {"class": "row"})

    res_list = []

    for i in test:
        if len(i.text.strip().split()) < i.text.strip().count(' '):
            res_list.append(re.sub(' +', ' ', i.text.strip().replace('\n', '')))
        else:
            res_list.append(i.text.strip().replace('\n', ''))
    try:
        return [res_list[1].split()[3], res_list[6]]
    except IndexError:
        return "I can't say when..."


def anime_description(title_url):
    result = requests.get(url=title_url)
    soup = BeautifulSoup(result.text, 'lxml')

    test = soup.find("div", {"class": "description pb-3"})
    description = test.text.strip().replace('\n', '')

    return description


def episode_counter(stats):
    res = []

    if stats[-1].endswith('?') or stats == "I can't say when...":
        return 'Idk the exact release date'
    else:
        for i in stats[-1].split('/'):
            res.append(int(i.strip()))

    return res


def final_episode_release_date(exe):
    week = {'пн': 0, 'вт': 1, 'ср': 2, 'чт': 3, 'пт': 4, 'сб': 5, 'вс': 6}

    today = date.today()

    if episode_counter(exe) == 'Idk the exact release date':
        return 'Idk the exact release date'
    counter = episode_counter(exe)[0]
    last_episode = episode_counter(exe)[1]
    release_day = exe[0]

    while counter != last_episode:
        if today.weekday() == week[release_day]:
            counter += 1
            if counter == last_episode:
                break
        today = today + timedelta(days=1)

    return today.strftime('%Y.%m.%d')
