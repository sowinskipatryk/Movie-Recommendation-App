from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import keyboard
import os
import time

DRIVER_PATH = r'C:\Program Files\chromedriver.exe'

LOGIN = os.environ['LOGIN']
PASSW = os.environ['PASSW']

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("--disable-extensions")
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

def login(url):
    driver = webdriver.Chrome(DRIVER_PATH, options=option)
    driver.maximize_window()

    driver.get(url)

    agree_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, 'didomi-notice-agree-button')))
    agree_button.click()

    time.sleep(5)

    try:
        skip_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ws__skipButton')))
        skip_button.click()
    except TimeoutException or NoSuchElementException:
        pass

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
    return driver
