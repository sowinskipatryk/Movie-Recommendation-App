from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import keyboard
import pandas as pd
import time
from page_login import login

movies = pd.read_excel('movieslist.xlsx', header=0)
matrix = pd.read_excel('ratings_matrix_entry.xlsx', index_col="Movie Id",
                       header=0)

movie_ids = movies['Movie Id']
links = movies['Link']

driver = login('http://filmweb.pl')

time.sleep(3)

id = 0
for url in links:
    driver.get(url+"#votes")

    time.sleep(5)

    try:
        sidebar_click = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME,
                                              'sidebarPanel__panel')))
        sidebar_click.click()

        a = ActionChains(driver)
        m = driver.find_element(By.CLASS_NAME, 'sidebarPanel__panel')
        a.move_to_element(m).perform()

    except TimeoutException or NoSuchElementException:
        pass

    time.sleep(3)

    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    review_num = int(soup.find('div',
                               {'class': 'ratingStats__users'})['data-total'])
    for i in range(review_num // 4):
        keyboard.press_and_release('page down')
        time.sleep(1.5)

    time.sleep(3)

    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    ratings = []
    reviews = soup.find_all('div', {'class': 'filmFriendCommentFilmVote'})
    with open(f'rates_{id+1}.txt', 'w', encoding='utf-8') as f:
        for review in reviews:
            username = review.find('a')['href'].split('/')[-1]
            rate = None
            try:
                rate = review.find('span', {'class': 'rate'}).text
                matrix[username].at[1048] = rate
            except AttributeError:
                print(f'No rating for username: {username}!')
            finally:
                print(f'Username: {username}\nRating: {rate}\n')
                f.write(f'{username} {rate}\n')
            ratings.append([username, rate])

    id += 1

    print(f'Number of ratings: {len(ratings)}')
    print(ratings)

matrix.to_excel('ratings_matrix_entry.xlsx')
driver.close()
