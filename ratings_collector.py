from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import keyboard
import pandas as pd
import time
from helper_funcions.page_login import login

movies = pd.read_excel('./excel_files/movies.xlsx', header=0)
friends = pd.read_excel('./excel_files/friends.xlsx', header=0)

usernames = friends['Username']
movie_ids = movies['Movie Id']
links = movies['Link']

matrix = pd.DataFrame(index=movie_ids, columns=usernames)

driver = login('http://filmweb.pl')

time.sleep(3)

id = 0 # Change it to start scraping at certain index
links = links[id:]
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
    rev = soup.find('div', {'class': 'ratingStats__users'})['data-total']
    if not rev:
        review_num = 0
    else:
        review_num = int(rev)

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
                pass
            finally:
                f.write(f'{username} {rate}\n')
            ratings.append([username, rate])

    id += 1

matrix.to_excel('./excel_files/ratings_matrix.xlsx')
driver.close()
