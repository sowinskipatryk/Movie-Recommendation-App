from bs4 import BeautifulSoup
import os
import pandas as pd
import time
from helper_functions.page_login import login

USERNAME = os.environ['USERNAME']

url = f"https://www.filmweb.pl/user/{USERNAME}/friends"

driver = login(url)
time.sleep(5)

driver.get(url)
time.sleep(10)

step = 1000
i = 1
flag = True
while flag:
    driver.execute_script(f"window.scrollTo(0, {i*step});")
    time.sleep(4)
    curr_page_height = driver.execute_script(
        "return document.body.scrollHeight")

    i += 1

    if i*step >= curr_page_height:
        flag = False

page_html = driver.page_source

soup = BeautifulSoup(page_html, 'html.parser')

friendslist = []
friend_section = soup.find('section', {'class': 'section__userFriends'})
friends = friend_section.find_all('div', {'class': 'user__body'})

for friend in friends:
    name = friend.find('span', {'class':'user__firstName'})
    if name:
        name = friend.find('span', {'class': 'user__firstName'}).text
    surname = friend.find('span', {'class': 'user__lastName'})
    if surname:
        surname = friend.find('span', {'class': 'user__lastName'}).text
    username = friend.find('a')['href'][6:]
    friendslist.append([name, surname, username])

df = pd.DataFrame(friendslist, columns=['Name', 'Surname', 'Username'],
                  index=range(1, len(friendslist)+1))
df.to_excel('./excel_files/friends.xlsx')

driver.close()
