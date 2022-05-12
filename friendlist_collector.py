from bs4 import BeautifulSoup
import time
import pandas as pd
from page_login import login

driver, url = login()
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

friends_list = []
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
    friends_list.append([name, surname, username])

df = pd.DataFrame(friends_list, columns=['Name', 'Surname', 'Username'],
                  index=range(1, len(friends_list)+1))
df.to_excel('friends_list.xlsx')

driver.close()
