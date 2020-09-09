from pprint import pprint
from lxml import html
import requests
import datetime
import json

now = datetime.datetime.now()
today = now.strftime("%d-%m-%Y")

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

# Работаем с сайтом news.mail.ru
main_link = 'https://news.mail.ru/'
response = requests.get(main_link ,headers=header)

dom = html.fromstring(response.text)

# Формируем DOM для всех колонок новостей, в каждой колонке есть главная новость (main_news) и три менее значимых новости (minor_news)
mail_news = []

# Обрабатываем все  main_news:
news_blocks = dom.xpath("//div[@class='cols__inner']")

# Обрабатываем все  main_news:
for item in news_blocks:
    one_news = {}
    main_news = item.xpath(".//span[@class='newsitem__title-inner']/text()")

    main_news_link = item.xpath(".//a[@class='newsitem__title link-holder']//@href")

    # получаем время публикации:
    response_2 = requests.get(main_news_link[0], headers=header)
    dom_news = html.fromstring(response_2.text)
    try:
        main_news_time = dom_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']//@datetime")
        date_news = main_news_time[0][0:10]
        time_news = main_news_time[0][11:16]
        main_news_time = date_news + ' ' + time_news
    except:
        main_news_time = 0

    one_news['news_source'] = 'news.mail.ru'
    one_news['main_news_name'] = main_news[0]
    one_news['main_news_name'] = one_news['main_news_name'].replace('\xa0', ' ')
    one_news['main_news_link'] = main_news_link[0]
    one_news['main_news_time'] = main_news_time

    mail_news.append(one_news)

# Обрабатываем все  minor_news:
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
    try:
        minor_news_time = dom_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']//@datetime")
        date_news = minor_news_time[0][0:10]
        time_news = minor_news_time[0][11:16]
        minor_news_time = date_news + ' ' + time_news
    except:
        minor_news_time = 0

    one_news['_news_source'] = 'news.mail.ru'
    one_news['minor_news_name'] = minor_news[0]
    one_news['minor_news_name'] = one_news['minor_news_name'].replace('\xa0', ' ')

    one_news['minor_news_link'] = minor_news_link[0]
    one_news['minor_news_time'] = minor_news_time


    mail_news.append(one_news)

# Работаем с сайтом https://lenta.ru/
main_link = 'https://lenta.ru/'
response = requests.get(main_link ,headers=header)

dom = html.fromstring(response.text)

#Формируем DOM для всех колонок новостей, в каждой колонке есть главная новость (main_news) и три менее значимых новости (minor_news)


#jОбрабатываем все  main_news:
news_blocks = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']")

#jОбрабатываем все  main_news:
for item in news_blocks:
    one_news = {}
    main_news = item.xpath(".//a/text()")


    main_news_link = item.xpath(".//a/@href")
    main_news_link = main_link + main_news_link[0]
    # main_news_date = item.xpath(".//a//time[@class='g-time']/@title")
    # main_news_time = item.xpath(".//a//time[@class='g-time']/@datetime")
    main_news_time = item.xpath(".//a//time[@class='g-time']/@datetime")
    main_news_time = today + ' ' + main_news_time[0][1:6]


    one_news['_news_source'] = 'lenta.ru'
    one_news['main_news_name'] = main_news[0]
    one_news['main_news_name'] = one_news['main_news_name'].replace('\xa0', ' ')
    one_news['main_news_link'] = main_news_link
    one_news['main_news_time'] = main_news_time

    mail_news.append(one_news)


# Работаем с сайтом https://yandex.ru/news/
main_link = 'https://yandex.ru/news/'
response = requests.get(main_link ,headers=header)

dom = html.fromstring(response.text)


#Формируем DOM для всех колонок новостей:


news_blocks = dom.xpath("//div[@class='mg-grid__col mg-grid__col_xs_4']")

for item in news_blocks:

    one_news = {}
    main_news = item.xpath(".//h2[@class='news-card__title']/text()")
    # проверка на рекламны блок:
    if len(main_news) >= 1:

        main_news_link = item.xpath(".//a/@href")[0]
        main_news_time = item.xpath(".//span[@class='mg-card-source__time']/text()")
        main_news_time = today + ' '+ main_news_time[0]


        one_news['_news_source'] = 'yandex.ru/news/'
        one_news['main_news_name'] = main_news[0]
        one_news['main_news_link'] = main_news_link
        one_news['main_news_time'] = main_news_time

        mail_news.append(one_news)


with open("news.json", "w") as write_file:
    json.dump(mail_news, write_file)


pprint(mail_news)
print(f'\nВсего выбрано {len(mail_news)} на трех новостных сайтах')