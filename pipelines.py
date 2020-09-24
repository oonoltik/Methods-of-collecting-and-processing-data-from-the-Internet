# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


from pymongo import MongoClient
from itemadapter import ItemAdapter

class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost',27017)
        #client.drop_database('vacancy160920')
        self.mongo_base = client.vacancy160920

    def process_item(self, item, spider):
        salary = item['salary']
        item['min_salary'] = None
        item['max_salary'] = None
        item['curency'] = None

        if spider.name == 'superjob_ru':
            print('ЗРП', salary)

            if 'руб.' in salary[-1]:
                item['curency'] = 'RUB'
            if '₽.' in salary[-1]:
                item['curency'] = 'RUB'

            if '€' in salary[-1]:
                item['curency'] = 'EUR'
            if '$' in salary[-1]:
                item['curency'] = 'USD'
            if 'грн.' in salary[-1]:
                item['curency'] = 'UAH'

            #item['salary_comment'] = None
            for i in salary:
                i = i.replace(u'\xa0', u'')
                i = i.replace('руб.', '')
                i = i.replace(' ', '')
            salary[0] = salary[0].replace(u'\xa0', u'')
            salary[0] = salary[0].replace(' ', '')
            print('ЗРП2', salary)

            if salary[0] == 'до':
                item['max_salary'] = salary[2]

            elif salary[0] == 'от':
                item['min_salary'] = salary[2]


            if len(salary) > 3 and salary[0].isdigit():
                item['min_salary'] = salary[0]
                item['max_salary'] = salary[2]
            elif len(salary) == 3 and salary[0].isdigit():
                item['max_salary'] = salary[0]



        elif spider.name == 'hhru':
            print()

            salary = item['salary']


            #if salary[0] == 'з/п не указана':

                #item['salary_comment'] = None
            if salary[0] == 'от ':
                if salary[2] == ' до ':
                    item['min_salary'] = salary[1]
                    item['max_salary'] = salary[3]
                    item['curency'] = salary[5]
                    item['salary_comment'] = salary[6]
                else:
                    item['min_salary'] = salary[1]
                    #item['max_salary'] = None
                    item['curency'] = salary[3]
                    item['salary_comment'] = salary[4]
            elif salary[0] == 'до ':
                #item['min_salary'] = None
                item['max_salary'] = salary[1]
                item['curency'] = salary[3]
                item['salary_comment'] = salary[4]




        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


        print()

