import requests
from bs4 import BeautifulSoup


# возвращает словарь онгоингов {название: ссылка}
def anime_ongoing_list():

    anime_title_href = {}

    for page in range(1, 5):
        url = f'https://animego.org/anime/status/ongoing?sort=a.createdAt&direction=desc&type=animes&page={page}'
        req_result = requests.get(url=url)
        soup = BeautifulSoup(req_result.text, 'lxml')

        check = soup.find(id="anime-list-container")

        anime_title = []
        anime_href = []

        try:
            for i in check:
                test = i.find("div", {"class": "h5 font-weight-normal mb-1"})
                for link in test('a', href=True):
                    anime_href.append(link['href'])
                for title in test:
                    anime_title.append(title.text)
        except TypeError:
            break

        anime_title_href.update(
            {anime_title[i]: anime_href[i] for i in range(len(anime_title))
             if requests.get(anime_href[i]).status_code != 404}
        )

    return anime_title_href



