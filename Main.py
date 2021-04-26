import bs4
import requests
import lxml
import re
import json
import time
import random

for i in range(1, 21):

    time.sleep(random.randrange(2,4))
    print("Итерация ", i)

    url = f'https://www.kinopoisk.ru/popular/films/?page={i}&tab=all'
    page = requests.get(url)

    print('Если далее 200, то запрос сработал, страничка скачалась: ', page.status_code)

    allFilms = []
    final_films_dict = []

    soup = bs4.BeautifulSoup(page.text, "html.parser")

    allFilms = soup.find_all('div', class_='desktop-rating-selection-film-item')


    # Filtering only good films 2020-2021. Saving to .json its name, year and href
    for data in allFilms:
        if data.find('span', class_='film-item-rating-position__diff film-item-rating-position__diff_sign_positive') is not None\
                and data.find('p', class_='selection-film-item-meta__original-name') is not None:

            original_name_year = data.find('p', class_='selection-film-item-meta__original-name').text
            year = "-".join(re.findall(r'\d+', original_name_year))
            name = data.find('p', class_='selection-film-item-meta__name').text
            ref = 'https://www.kinopoisk.ru' + data.find(class_='selection-film-item-meta__link').get('href')

            film_dict = {
                'name': name,
                'year': year,
                'ref': ref
            }

            if "2021" in year or "2020" in year:
                final_films_dict.append(film_dict)
                print(film_dict)

                with open("data/good_new_films.json", "a", encoding="utf-8") as file1:
                    json.dump(film_dict, file1, ensure_ascii=False)





