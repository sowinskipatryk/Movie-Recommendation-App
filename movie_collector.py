import requests
from bs4 import BeautifulSoup
import pandas as pd

urls = [f'https://www.filmweb.pl/ajax/ranking/film/{i}' for i in range(1,21)]

movies = []
for url in urls:
    movie = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all('div', {'class': 'rankingType'})
    for item in items:
        title = item.find('h2').text
        link = 'https://www.filmweb.pl' + item.find('a')['href']
        original_title = item.find('p', {'class':'rankingType__originalTitle'}
                                   ).text[:-5]
        year = item.find('p', {'class':'rankingType__originalTitle'}).text[-4:]
        genre = item.find('div', {'class':'rankingType__genres'}).text[7:]
        movie_id = link.split('-')[-1]
        if not original_title:
            original_title = title
        movie = [title, original_title, genre, year, link, movie_id]
        movies.append(movie)

df = pd.DataFrame(movies, columns=['Title', 'Original Title', 'Genre', 'Year',
                                   'Link', 'Movie Id'], index=range(1,501))

df.to_excel('movieslist.xlsx')