from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
import time

from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
from pandas.io import sql
import sqlite3

# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
#
# driver = webdriver.Chrome(ChromeDriverManager().install())

# парсим через Chrome
chrome_options = Options()

# !!! Обязательно открываем полную страницу, иначе не отображаются кнопки прокрутки для дальнейшего перехода
chrome_options.add_argument('start-maximized')

# задаем драйвер и стартовую страницу

name = 'study.ai_172@mail.ru'
password = 'NextPassword172'

driver = webdriver.Chrome()
driver.get('https://mail.ru/')
# driver.find_element_by_id('mailbox:login-input')
mail_name = driver.find_element_by_id('mailbox:login-input')

password_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="mailbox:submit-button"]')))
enter_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="o-control"]')))
mail_name.send_keys(name)
password_button.click()

time.sleep(1)

mail_pass = driver.find_element_by_id('mailbox:password-input')
mail_pass.send_keys(password)
mail_pass.send_keys(Keys.RETURN)

# Ищем блоки с письмами
time.sleep(5)
assert "Входящие - Почта Mail.ru" in driver.title

first_mail_block = driver.find_element_by_class_name('llc__container')
actions = ActionChains(driver)
actions.click(first_mail_block)
actions.perform()

next_mail_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="button2 button2_has-ico button2_arrow-down button2_pure button2_short button2_ico-text-top button2_hover-support js-shortcut"]'))
    )
all_mails =[]
num = 1
control = 0
stop_featute = 1
while stop_featute == 1:
    one_mail ={}
    print(num)
    wait = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'letter__body'))
                                           )
    time.sleep(0.5)

    try:
        wait = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'thread__subject-line'))
             )
        one_mail['one_mail_topic'] = driver.find_element_by_class_name('thread__subject-line').text
        print(one_mail['one_mail_topic'])
    except:
        one_mail['one_mail_topic'] = None
        print(num, one_mail['one_mail_topic'])

    try:

        wait = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'letter-contact'))
        )

        sender_info = driver.find_element_by_class_name('letter-contact')
        one_mail['one_mail_sender_name'] = sender_info.text
        print(one_mail['one_mail_sender_name'])
        one_mail['one_mail_sender_email'] = sender_info.get_attribute('title')
        print(one_mail['one_mail_sender_email'])
    except:
        one_mail['one_mail_sender_name'] = None
        one_mail['one_mail_sender_email'] = None

        print(num, one_mail['one_mail_sender_name'], one_mail['one_mail_sender_email'])

    try:

        wait = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'letter__date'))
        )
        one_mail['one_mail_date'] = driver.find_element_by_class_name('letter__date').text
        print(one_mail['one_mail_date'])
    except:
        one_mail['one_mail_date'] = None
        print(num, one_mail['one_mail_date'])

    try:
        # wait = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'letter__body'))
        #     )
        one_mail['one_mail_text'] = driver.find_element_by_class_name('letter__body').text
        print(one_mail['one_mail_text'])
    except:
        one_mail['one_mail_text'] = None
        print(num, one_mail['one_mail_text'])

    all_mails.append(one_mail)
    #print(one_mail)

    # проверка на последнее письмо:
    try:
        next_mail_button.click()
    except:
        print("Письма закончились")
        stop_featute = 0

    
    num +=1

# формируем файл _json
with open("All_mails_json.json", "w") as write_file:
    json.dump(all_mails, write_file)
driver.close()


# Формируем базу all_hits :
engine = create_engine('sqlite:///all_mails.db',echo=True)

Base = declarative_base()

class All_mails(Base):
    __tablename__ = 'all_mails'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    one_mail_sender_name = Column(String(255))
    one_mail_sender_email = Column(String(255))
    one_mail_date = Column(String(255))
    one_mail_text = Column(String(255))



    def __init__(self, one_mail_date, one_mail_sender_name, one_mail_sender_email, one_mail_text):

        self.one_mail_date = one_mail_date
        self.one_mail_sender_name = one_mail_sender_name
        self.one_mail_sender_email = one_mail_sender_email
        self.one_mail_text = one_mail_text

# Делаем Датафрейм из полученной после парсинга базы:
df = pd.read_json('All_mails_json.json')
# Сохраняем датафрем в базу
df.to_sql(con=engine, index_label='id', name=All_mails.__tablename__, if_exists='replace')