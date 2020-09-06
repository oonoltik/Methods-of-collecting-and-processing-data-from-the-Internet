from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

'''Вносим название вакансии'''
#vacancy_name = 'data scientist'


vacancy_name = input("Введите назавние вакансии:")

# data scientist

print(vacancy_name)


'''Работаем с сайтом HH'''

# def hh_one_page_finder(vacancy_name):
vacancy_name_hh = vacancy_name.replace(' ', '+')
main_link = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&search_field=name&text='
link_add = '&page='
link_num = 0
go_on = 'дальше'
vacancies = []
num = 1

while go_on == 'дальше':

    '''Формируем стратовый  линк для поиска на HH:'''


    start_link = main_link + vacancy_name_hh + link_add + str(link_num)
    print(start_link)

    ''' Задаем headers'''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    '''Формируем soup:'''
    response = requests.get(start_link, headers=headers)
    soup = bs(response.text,'html.parser')


    '''Формируем список из всех элментов содержащих название и описание вакансии:'''
    vacancies_list = soup.find_all('div', class_='vacancy-serp-item')


    '''Работаем с каждым элментом полученного списка и получаем значения: линк, наименование вакансии, наименование работодателя, адрес работодателя, вилку по предлагаемой ЗРП, описание обязаннотсей '''



    for vacancy in vacancies_list:
        vanacy_data={}
        vanacy_link = vacancy.find('a', class_='bloko-link HH-LinkModifier').get('href')
        try:
            employer_name = vacancy.find('a', class_='bloko-link bloko-link_secondary').getText()
        except:
            employer_name = None
        try:
            employer_adress = vacancy.find('span', class_='vacancy-serp-item__meta-info').getText()
        except:
            employer_adress = None

        vacancy_title = vacancy.find('a', class_='bloko-link HH-LinkModifier').getText()
        vacancy_responsibility = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).getText()
        vacancy_requirement = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).getText()

        '''Получаем и Обрабатываем данные по зарплате:'''
        salary_row = vacancy.find('div', class_='vacancy-serp-item__sidebar').getText()
        salary_row = salary_row.replace(' ', '')
        salary_row = salary_row.replace(' ', '')

        ''' Определеям в какой валюте определенеа зарплата'''
        try:
            if 'бел.' in salary_row:
                salary_currency = 'Белорусский рубль'
                salary_row = salary_row.replace('бел.', '').replace('руб.', '')
            if 'руб.' in salary_row:
                salary_currency = 'Рублей'
                salary_row = salary_row.replace('руб.', '')
            elif 'EUR' in salary_row:
                salary_currency = 'Евро'
                salary_row = salary_row.replace('EUR', '')
            elif 'USD' in salary_row:
                salary_currency = 'Долларов США'
                salary_row = salary_row.replace('USD', '')
            elif 'KZT' in salary_row:
                salary_currency = 'Казахский тенге'
                salary_row = salary_row.replace('KZT', '')
            elif 'сум' in salary_row:
                salary_currency = 'Узбексий сум'
                salary_row = salary_row.replace('сум', '')

            elif 'грн.' in salary_row:
                salary_currency = 'Украинская гривна'
                salary_row = salary_row.replace('грн.', '')
            elif 'KGS' in salary_row:
                salary_currency = 'Киргизский сом'
                salary_row = salary_row.replace('KGS', '')
            else:
                salary_currency = None
        except:
            salary_currency = None



        try:
            if '-' in salary_row:
                sal_list = salary_row.split('-')
                salary_start = sal_list[0]
                salary_finish = sal_list[1]


            else:
                if 'от' in salary_row:
                    salary_start = salary_row.replace('от', '')
                    salary_finish = 0


                elif 'до' in salary_row:
                    salary_finish = salary_row.replace('до', '')
                    salary_start = 0


                if salary_row == '':
                    salary_start = 0
                    salary_finish = 0
        except:
            salary_start = 0
            salary_finish = 0


        if 'hh.ru' in vanacy_link:
            site_name = "Хэдхантер"
        elif 'superjob.ru' in vanacy_link:
            site_name = "Superjob"
        else:
            site_name = "Сайт не определен"

        '''Добавляем значения для каждой вакансии в виде словаря'''

        vanacy_data['#number'] = num
        vanacy_data['site_name'] = site_name
        vanacy_data['link'] = vanacy_link
        vanacy_data['vacancy_title'] = vacancy_title
        vanacy_data['employer'] = employer_name
        vanacy_data['employer_adress'] = employer_adress
        vanacy_data['salary_currency'] = salary_currency
        vanacy_data['salary_start'] = int(salary_start)
        vanacy_data['salary_finish'] = int(salary_finish)
        vanacy_data['vacancy_responsibility'] = vacancy_responsibility
        vanacy_data['vacancy_requirement'] = vacancy_requirement

        ''' Формируем конечный список из словарей HH'''
        vacancies.append(vanacy_data)

        num += 1
    try:
        go_on = soup.find('a', class_='bloko-button HH-Pager-Controls-Next HH-Pager-Control').getText()
    except:
        go_on = 0

    link_num += 1

    #return (vacancies)







'''Работаем с сайтом Superjob'''

#vacancy_name = input("Введите назавние вакансии:")

# data scientist

'''При работе с сылками в формате https://www.superjob.ru/vakansii/direktor-po-it.html?noGeo=1 -
используем транслетерацию русских букв в английские:'''
'''slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
          'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
          'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
          'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
          'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
          'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
          'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
          'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
          'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
          '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
          ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
          '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
          'Є': 'e', '—': ''}'''

# Циклически заменяем все буквы в строке
#for key in slovar:
#    vacancy_name = vacancy_name.replace(key, slovar[key])

#vacancy_name = vacancy_name.replace('_', '-')
#vacancy_name = vacancy_name.lower()

'''Решили использовать формат ссылок https://www.superjob.ru/vacancy/search/?keywords=менеджер%20по%20персоналу&noGeo=1&page=2
что позволяет медленее, но с большей точностью искать вакансии'''

vacancy_name_sj = vacancy_name.replace(' ', '%20')

main_link = 'https://www.superjob.ru'
#link_add_0 = '/vakansii/'
link_add_0 = '/vacancy/search/?keywords='
link_add = '&noGeo=1&page='
link_num = 1

'''Определяем стартовую нумерацию для сайта Superjob'''
#vacancies = []
num = vacancies[-1]["#number"] + 1
go_on = 'Дальше'


while go_on == 'Дальше':
    start_link = main_link + link_add_0 + vacancy_name_sj + link_add + str(link_num)
    print(start_link)

    '''Формируем soup:'''
    response = requests.get(start_link, headers=headers)
    soup = bs(response.text, 'html.parser')

    '''Формируем список из всех элментов содержащих название и описание вакансии:'''
    vacancies_list = soup.find_all('div', class_='iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL')


    for vacancy in vacancies_list:
        vanacy_data = {}
        vanacy_link = vacancy.find('div', class_='_3mfro PlM3e _2JVkc _3LJqf')
        vanacy_link = vanacy_link.find('a').get('href')
        vanacy_link = main_link + vanacy_link

        try:
            employer_name = vacancy.find('span', class_='_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI').getText()
        except:
            employer_name = None

        try:
            employer_adress = vacancy.find('span', class_='_3mfro f-test-text-company-item-location _9fXTd _2JVkc _2VHxz').getText()
            employer_adress = employer_adress.split('•')
            employer_adress = employer_adress[1]
        except:
            employer_adress = None

        vacancy_title = vacancy.find('div', class_='_3mfro PlM3e _2JVkc _3LJqf').getText()

        try:
            vacancy_descr = vacancy.find('span', class_='_3mfro _38T7m _9fXTd _2JVkc _2VHxz _15msI').getText()
            if '…' in vacancy_descr:
                vacancy_descr = vacancy_descr.split('…')
                vacancy_responsibility = vacancy_descr[0]
                vacancy_requirement = vacancy_descr[1]
            else:
                vacancy_responsibility = vacancy_descr
                vacancy_requirement = None
        except:
            vacancy_responsibility = None
            vacancy_requirement = None

        '''Получаем и Обрабатываем данные по зарплате:'''
        salary_row = vacancy.find('span', class_='_3mfro _2Wp8I PlM3e _2JVkc _2VHxz').getText()
        salary_row = salary_row.replace(' ', '')
        salary_row = salary_row.replace(' ', '')


        ''' Определеям в какой валюте определенеа зарплата'''
        try:
            if 'бел.' in salary_row:
                salary_currency = 'Белорусский рубль'
                salary_row = salary_row.replace('бел.', '').replace('руб.', '')
            if 'руб.' in salary_row:
                salary_currency = 'Рублей'
                salary_row = salary_row.replace('руб.', '')
            elif 'EUR' in salary_row:
                salary_currency = 'Евро'
                salary_row = salary_row.replace('EUR', '')
            elif 'USD' in salary_row:
                salary_currency = 'Долларов США'
                salary_row = salary_row.replace('USD', '')
            elif 'KZT' in salary_row:
                salary_currency = 'Казахский тенге'
                salary_row = salary_row.replace('KZT', '')
            elif 'сум' in salary_row:
                salary_currency = 'Узбексий сум'
                salary_row = salary_row.replace('сум', '')
            elif 'грн.' in salary_row:
                salary_currency = 'Украинская гривна'
                salary_row = salary_row.replace('грн.', '')
            elif 'KGS' in salary_row:
                salary_currency = 'Киргизский сом'
                salary_row = salary_row.replace('KGS', '')

            else:
                salary_currency = None
        except:
            salary_currency = None


        try:
            salary_start = salary_row
            salary_finish = salary_row

            if '—' in salary_row:
                sal_list = salary_row.split('—')
                salary_start = sal_list[0]
                salary_finish = sal_list[1]


            else:
                if 'от' in salary_row:
                    salary_start = salary_row.replace('от', '')
                    salary_finish = 0


                elif 'до' in salary_row:
                    salary_finish = salary_row.replace('до', '')
                    salary_start = 0

                if salary_row == '' or salary_row == 'Подоговорённости':
                    salary_start = 0
                    salary_finish = 0

        except:
            salary_start = 0
            salary_finish = 0

        if 'hh.ru' in vanacy_link:
            site_name = "Хэдхантер"
        elif 'superjob.ru' in vanacy_link:
            site_name = "Superjob"
        else:
            site_name = "Сайт не определен"

        vanacy_data['#number'] = num
        vanacy_data['link'] = vanacy_link
        vanacy_data['employer'] = employer_name
        vanacy_data['employer_adress'] = employer_adress
        vanacy_data['salary_currency'] = salary_currency
        vanacy_data['salary_start'] = int(salary_start)
        vanacy_data['salary_finish'] = int(salary_finish)
        vanacy_data['site_name'] = site_name
        vanacy_data['vacancy_title'] = vacancy_title
        vanacy_data['vacancy_responsibility'] = vacancy_responsibility
        vanacy_data['vacancy_requirement'] = vacancy_requirement


        vacancies.append(vanacy_data)
        num += 1

    try:
        go_on = soup.find('div', class_='_3zucV L1p51 undefined _1Fty7 _2tD21 _3SGgo')
        go_on = go_on.find_all('span', class_='_3IDf-')
        go_on = go_on[-1].getText()
    except:
        go_on = 0


    link_num += 1

# a = hh_one_page_finder(vacancy_name)
pprint(vacancies)

'''Можно записать полученую базу в csv'''
import csv
# with open(r'C:\Users\Newman\Google Диск\Geekbrains\Методы сбора и обработки данных из сети Интернет\121.csv', 'w', encoding='utf-8-sig') as csvfile:
with open('121.csv', 'w', encoding='utf-8-sig') as csvfile:
    fieldnames = ['#number', 'link', 'employer', 'employer_adress', 'salary_currency', 'salary_start', 'salary_finish', 'site_name', 'vacancy_title', 'vacancy_responsibility', 'vacancy_requirement']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(vacancies)

import pandas as pd

print(pd.DataFrame(vacancies))

import json
with open("HH_SJ_vacancies.json", "w") as write_file:
    json.dump(vacancies, write_file)





