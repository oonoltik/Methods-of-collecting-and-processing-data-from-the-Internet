
values = ['\n                Жилое помещение\n                \n            ', '\n                150.0\n                \n            ', '\n                230.0\n                \n            ', '\n                45.0\n                \n            ', '\n                2300x1500x45\n                \n            ', '\n                61600\n                \n            ', '\n                48.0\n                \n            ', '\n                1780\n                \n            ', '\n                2700.0\n                \n            ', '\n                Прямоугольный\n                \n            ', '\n                Кремовый\n                \n            ', '\n                Бежевый\n                \n            ', '\n                Шарм\n                \n            ', '\n                Россия\n                \n            ', '\n                100% ПП Freze\n                \n            ', '\n                Джут\n                \n            ', '\n                Полипропилен\n                \n            ', '\n                Нет\n                \n            ', '\n                MERINOS\n                \n            ', '\n                Отсутствует\n                \n            ', '\n                Пылесос\n                \n            ', '\n                Термоусадочная упаковка\n                \n            ', '\n                8.994\n                \n            ', '\n                Ковер\n                \n            ']

values_2 = []
for i in values:
    print(i)
    i = i.replace('\n', '')
    i = i.replace('  ', '')

    # i.strip()
    # i.replace("\n", "*")
    # i.rstrip()
    # i.join(i.split())
    print(i)
    values_2.append(i)


print(values)
print(values_2)