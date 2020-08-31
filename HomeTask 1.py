
''' 1. Посмотреть документацию к API GitHub, разобраться как вывести
список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.'''

from pprint import pprint
import requests
import json

url = 'https://api.github.com'
user='oonoltik'

appid = '4c265b2472c6f2131f0a40434469913517f62231'


r = requests.get(f'{url}/users/{user}/repos')

with open('data.json', 'w') as f:
    json.dump(r.json(), f)

print(f'Список репозиториев пользователя {user}:')
for i in r.json():
    print(i['name'])
print('\n')

'''2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). 
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.'''

API_KEY = '069afb29-fba1-49fd-8c18-2ba9fee4ed91'

def get_address(lat, lon):

    URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={lat},{lon}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU"
    result = requests.get(URL).json()
    return result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

lat = '55.760241'
lon = '37.611347'
e = get_address(lat, lon)

print(f'Адресом обьекта с долготой {lon} и широтой {lat} является: {e} \n')

r = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={lat},{lon}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU")
j_data = r.json()
print('Сохраняемый в файл yandex_map.json :\n')
pprint(j_data)
with open('yandex_map.json', 'w') as f:
    json.dump(r.json(), f)