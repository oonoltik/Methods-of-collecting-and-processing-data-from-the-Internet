from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import pandas as pd
from pandas.io import sql
import sqlite3



# Формируем базу vacancies2 :
engine = create_engine('sqlite:///vacancies2.db',echo=True)  # pass your db url
# cnx = sqlite3.connect(':memory:')
# df.to_sql(name='df', con=cnx)

Base = declarative_base()

class Vacancies(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    #number = Column(Integer)
    site_name = Column(String(255))
    link = Column(String(255))
    vacancy_title = Column(String(255))
    employer = Column(String(255))
    employer_adress = Column(String(255))
    salary_currency = Column(String(255))
    salary_start = Column(Integer)
    salary_finish = Column(Integer)
    vacancy_responsibility = Column(String(255))
    vacancy_requirement = Column(String(255))

    def __init__(self, site_name, link, vacancy_title, employer, employer_adress, salary_currency, salary_start, salary_finish, vacancy_responsibility, vacancy_requirement):
        #self.number = number
        self.site_name = site_name
        self.link = link
        self.vacancy_title = vacancy_title
        self.employer = employer
        self.employer_adress = employer_adress
        self.salary_currency = salary_currency
        self.salary_start = salary_start
        self.salary_finish = salary_finish
        self.vacancy_responsibility = vacancy_responsibility
        self.vacancy_requirement = vacancy_requirement


# Делаем Датафрейм из полученной после парсинга базы:
file_name = '121.csv'
df = pd.read_csv(file_name)
# Сохраняем датафрем в базу
df.to_sql(con=engine, index_label='id', name=Vacancies.__tablename__, if_exists='replace')

# Работаем с базой с READ запросами:
DBSession = sessionmaker(bind=engine)
session = DBSession()
num = 1
for object in session.query(Vacancies).all():
    print(object.vacancy_title, object.salary_start)
    print(num)
    num +=1

for object in session.query(Vacancies).filter(Vacancies.salary_start > 100000):
    print(object.vacancy_title, object.salary_start, object.salary_currency, object.employer, object.employer_adress)

session.commit()
session.close()