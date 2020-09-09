import timeit
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import csv
import re
from pprint import pprint
from lxml import html
import datetime
import json



header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15/0fcQXwPG-6'}
main_link = 'https://news.mail.ru/'
response = requests.get(main_link, headers=header)


# Таймер для xpath
a_xpath = timeit.default_timer()
# Работаем с сайтом news.mail.ru


dom = html.fromstring(response.text)

#Формируем DOM для всех колонок новостей, в каждой колонке есть главная новость (main_news) и три менее значимых новости (minor_news)
mail_news = []

#jОбрабатываем все  main_news:
news_blocks = dom.xpath("//div[@class='cols__inner']")

#jОбрабатываем все  main_news:
for item in news_blocks:
    one_news = {}
    main_news = item.xpath(".//span[@class='newsitem__title-inner']/text()")
    for n in main_news:
        for i in n:
            i.replace('\xa0', ' ')
    main_news_link = item.xpath(".//a[@class='newsitem__title link-holder']//@href")
    #main_news_time = item.xpath(".//span[@class='newsitem__param js-ago']//@datetime")
    # получаем время публикации:
    response_2 = requests.get(main_news_link[0], headers=header)
    dom_news = html.fromstring(response_2.text)
    main_news_time = dom_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']//@datetime")
    try:
        date_news = main_news_time[0][0:10]
        time_news = main_news_time[0][11:19]
        main_news_time = date_news + ' ' + time_news
    except:
        main_news_time = 0

    one_news['news_source'] = 'news.mail.ru'
    one_news['main_news_name'] = main_news
    one_news['main_news_link'] = main_news_link
    one_news['main_news_time'] = main_news_time

    mail_news.append(one_news)

#jОбрабатываем все  minor_news:
minor_news_blocks = dom.xpath("//span[@class='list__text']")

for item in minor_news_blocks:
    one_news = {}
    minor_news = item.xpath(".//span[@class='link__text']/text()")
    for n in minor_news:
        for i in n:
            i.replace('\xa0', ' ')
    minor_news_link = item.xpath(".//a[@class='link link_flex']//@href")

    # получаем время публикации:
    response_2 = requests.get(minor_news_link[0], headers=header)
    dom_news = html.fromstring(response_2.text)
    minor_news_time = dom_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']//@datetime")
    try:
        date_news = minor_news_time[0][0:10]
        time_news = minor_news_time[0][11:19]
        minor_news_time = date_news + ' ' + time_news
    except:
        minor_news_time = 0
    # print(minor_news_time)
    # print(date_news)
    # print(time_news)

    one_news['_news_source'] = 'news.mail.ru'
    one_news['minor_news_name'] = minor_news
    one_news['minor_news_link'] = minor_news_link
    one_news['minor_news_time'] = minor_news_time

    mail_news.append(one_news)
with open("news__Xpath.json", "w") as write_file:
    json.dump(mail_news, write_file)


timer_total_Xpath = timeit.default_timer() - a_xpath

pprint(mail_news)

print(f'\nВремя на обрабоку методом Хpath', timer_total_Xpath, '\n')



# Таймер для BeautifulSoup
a_BS = timeit.default_timer()

soup = bs(response.text,'html.parser')
news_blocks = soup.find_all('div', class_ = 'cols__inner')

#jОбрабатываем все  main_news:
for item in news_blocks:
    one_news = {}
    main_news = item.find('span', class_ = 'newsitem__title-inner').getText()
    for n in main_news:
        n.replace('\xa0', ' ')
    main_news_link = item.find('a', class_='newsitem__title link-holder').get('href')

    # получаем время публикации:
    response_2 = requests.get(main_news_link, headers=header)
    soup_2 = bs(response_2.text,'html.parser')
    try:

        main_news_time = soup_2.find('span', class_='note__text breadcrumbs__text js-ago').get('datetime')
        # main_news_time = main_news_time.get('datetime')
        date_news = main_news_time[0:10]
        time_news = main_news_time[11:19]
        main_news_time = date_news + ' ' + time_news
    except:
        main_news_time = 0



    one_news['news_source'] = 'news.mail.ru'
    one_news['main_news_name'] = main_news
    one_news['main_news_link'] = main_news_link
    one_news['main_news_time'] = main_news_time

    mail_news.append(one_news)



#jОбрабатываем все  minor_news:
minor_news_blocks = soup.find_all('span', class_ = 'list__text')


for item in minor_news_blocks:
    one_news = {}
    minor_news = item.getText()

    for n in minor_news:
        n.replace('\xa0', ' ')
    minor_news_link = item.find('a', class_='link link_flex').get('href')
    # find('a', class_='link link_flex')

    # получаем время публикации:
    response_2 = requests.get(minor_news_link, headers=header)

    soup_2 = bs(response_2.text, 'html.parser')
    try:

        minor_news_time = soup_2.find('span', class_='note__text breadcrumbs__text js-ago').get('datetime')
        # main_news_time = main_news_time.get('datetime')
        date_news = minor_news_time[0:10]
        time_news = minor_news_time[11:19]
        minor_news_time = date_news + ' ' + time_news
    except:
        minor_news_time = 0


    one_news['_news_source'] = 'news.mail.ru'
    one_news['minor_news_name'] = minor_news
    one_news['minor_news_link'] = minor_news_link
    one_news['minor_news_time'] = minor_news_time

    mail_news.append(one_news)

with open("news__BS.json", "w") as write_file:
    json.dump(mail_news, write_file)


timer_total_BS = timeit.default_timer() - a_BS
time_difference = timer_total_BS - timer_total_Xpath

pprint(mail_news)

print(f'\nВремя на обрабоку методом Хpath', timer_total_Xpath, '\n')
print(f'\nВремя на обрабоку методом BS', timer_total_BS, '\n')
print(f'\nРазница во времени timer_total_BS - timer_total_Xpath:', time_difference, '\n')
if time_difference > 0:
    print("По времени выиграл метод Xpath")
else:
    print("По времени выиграл метод BS")

