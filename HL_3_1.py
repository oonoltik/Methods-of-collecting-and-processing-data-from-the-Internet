from pymongo import MongoClient
from pprint import pprint
import json


#загружаем готовый json файл (полученый при выпонении ДЗ к 2 УРоку)
with open("HH_SJ_vacancies.json", "r") as read_file:
    data = json.load(read_file)

# формируем базу данных :
client = MongoClient('127.0.0.1',27017)
db = client['HH_SJ_db']

vacancies = db.vacancies


#функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта:
# проверяем наличие в базе идентичных записей по равенству полей: Название ваканчии, работодатель, начальная и конечная ЗРП
# Если такая запись есть - не вносим ее, если нет - вносим в базу
duplicates = 0
for i in data:

    numer = 0
    vacancy_title_i = i['vacancy_title']
    employer_i = i['employer']
    salary_start = i['salary_start']
    salary_finish_i = i['salary_finish']
    number_data = i['#number']

    for vc in vacancies.find({'$and': [{"vacancy_title": vacancy_title_i}, {"employer": employer_i}, {"salary_start": salary_start}, {"salary_finish": salary_finish_i}]}):
        numer += 1
        print(f'Обнаружен дубликат, номер записи в исходном json_файле: {number_data}','\n', vc,'\n',i)
        duplicates +=1

        # Делаем апдейт старых записей на новые (может быть там функционал или обязанности новые)
        vacancies.replace_one({'$and': [{"vacancy_title": vacancy_title_i}, {"employer": employer_i}, {"salary_start": salary_start}, {"salary_finish": salary_finish_i}]}, i)
        # print(f'Произведена замена:', vacancies.find_one({'$and': [{"vacancy_title": vacancy_title_i}, {"employer": employer_i}, {"salary_start": salary_start}, {"salary_finish": salary_finish_i}]}))


    if numer == 0:
        vacancies.insert_one(i)
        print(f'Сделана запись в базу, номер записи в исходном json_файле: :{number_data}')




for user in vacancies.find({}):
     pprint(user)
print(f'При дополнении базы обработано {duplicates} дублирующих записей')

# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введенной суммы. Поиск по двум полям (мин и макс зарплату)

#salary_limit = 400000
print('\nПроизводим поиск и вывод на экран вакансий с заработной платой больше введенной суммы. Поиск по двум полям (мин и макс зарплату)\n')
salary_limit = int(input('\nВведите желаемый уровень зарплаты:'))
print('\n\n============================================================================\n')
num = 0
for vc in vacancies.find({'$or': [ {"salary_start": {'$gte' : salary_limit}}, {"salary_finish": {'$gte' : salary_limit}}]}):
    pprint(vc)
    print('\n')
    num +=1
print(f'Количество вакансий с заданым уровнем Зарплаты ({salary_limit} руб/мес) в базе составило:', num, '  -- Вакансии перечислены выше')

vacancies.delete_many({})


