from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json

from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
from pandas.io import sql
import sqlite3

# парсим через Chrome
chrome_options = Options()

# !!! Обязательно открываем полную страницу, иначе не отображаются кнопки прокрутки для дальнейшего перехода
chrome_options.add_argument('start-maximized')

# задаем драйвер и стартовую страницу
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')

# Делаем итерцацию. Всего 4 страницы по Новинкам. Сейчас срабаотает и просто вариант с пролистыванием страниц
# и затем собиаем данные по всем блокам, но возможно разработчики уберут такую возможность.
# Мы перестраховались и парсим каждую страницу отдельно
pages = 0
while pages < 5:
    try:
        print(pages)

        # определяем блок с Хитами продаж
        bestsellers = driver.find_element_by_xpath(
            '//div[contains(text(),"Хиты продаж")]/ancestor::div[@data-init="gtm-push-products"]'
        )
        # определяем блоки с товарами
        goods = bestsellers.find_elements_by_css_selector('li.gallery-list-item')

        # скролим до блока с товарами (чтобы проявилась кнопка прокрутки)
        actions = ActionChains(driver)
        actions.move_to_element(bestsellers).perform()

        # обрабатываем каждай блок с выделением значимых арактеристик для переноса в базупарсим через Chrome
        all_hits = []
        for good in goods:
            item = {}
            item['title'] = good.find_element_by_css_selector(
                'a.sel-product-tile-title') \
                .get_attribute('innerHTML')

            item['good_link'] = good.find_element_by_css_selector(
                'a.sel-product-tile-title') \
                .get_attribute('href')

            item['price'] = float(
                good.find_element_by_css_selector(
                    'div.c-pdp-price__current').get_attribute('innerHTML').replace(
                    '&nbsp;', '').replace('¤', ''))

            item['image_link'] = good.find_element_by_css_selector(
                'img[class="lazy product-tile-picture__image"]') \
                .get_attribute('src')

            all_hits.append(item)
            print(item)

        # определяем кнопку перехода и  кликаем по ней
        try:
            next_button = WebDriverWait(bestsellers, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]'))
            )
        # next_button = bestsellers.find_element_by_css_selector('a.next-btn sel-hits-button-next')
            next_button.click()

        except:
            print(f'Кончились страницы, последняя страницы {pages}')

        pages += 1
    except Exception as e:
        print('Сбор окончен или что-то пошло не так')
        print(e.message)


print(all_hits)

# формируем файл _json
with open("HL_5_1_selenium_json.json", "w") as write_file:
    json.dump(all_hits, write_file)

driver.close()


# Формируем базу all_hits :
engine = create_engine('sqlite:///all_hits.db',echo=True)

Base = declarative_base()

class All_hits(Base):
    __tablename__ = 'all_hits'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(String(255))
    good_link = Column(String(255))
    price = Column(Integer)
    image_link = Column(String(255))


    def __init__(self, title, good_link, price, image_link):
        #self.number = number
        self.title = title
        self.good_link = good_link
        self.price = price
        self.image_link = image_link

# Делаем Датафрейм из полученной после парсинга базы:
df = pd.read_json('HL_5_1_selenium_json.json')
# Сохраняем датафрем в базу
df.to_sql(con=engine, index_label='id', name=All_hits.__tablename__, if_exists='replace')