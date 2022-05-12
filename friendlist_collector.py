from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import keyboard
import pandas as pd
import os

DRIVER_PATH = r'C:\Program Files\chromedriver.exe'

USERNAME = os.environ['USERNAME']
LOGIN = os.environ['LOGIN']
PASSW = os.environ['PASSW']

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("--disable-extensions")
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

driver = webdriver.Chrome(DRIVER_PATH, options=option)
driver.maximize_window()

url = f"https://www.filmweb.pl/user/{USERNAME}/friends"

driver.get(url)

agree_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.ID, 'didomi-notice-agree-button')))
agree_button.click()

time.sleep(5)

skip_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CLASS_NAME, 'ws__skipButton')))
skip_button.click()

time.sleep(10)

facebook_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CLASS_NAME, 'facebookLoginButton__text')))
facebook_login.click()

time.sleep(5)

allow_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]')))
allow_cookies.click()

time.sleep(5)

login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@type='text']")))
login.click()
keyboard.write(LOGIN)
passw = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@type='password']")))
passw.click()
keyboard.write(PASSW)
keyboard.press_and_release('enter')

time.sleep(5)

driver.get(url)

time.sleep(10)

step = 1000
i = 1
flag = True
while flag:
    driver.execute_script(f"window.scrollTo(0, {i*step});")
    time.sleep(1.5)
    curr_page_height = driver.execute_script(
        "return document.body.scrollHeight")

    i += 1

    if i*step >= curr_page_height:
        flag = False

page_html = driver.page_source

soup = BeautifulSoup(page_html, 'html.parser')

friendslist = []
friends = soup.find_all('div', {'class': 'user__body'})
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
df.to_excel('friendslist.xlsx')

driver.close()
