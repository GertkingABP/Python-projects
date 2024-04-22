# импорт библиотек
from bs4 import BeautifulSoup   # библиотека для парсинга
import pymysql  # для связи с mysql
import os
import datetime
import requests
import re

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

import lxml

def insert_sentence(col1):
    # вставка в таблицу бд
    con = pymysql.connect(host='localhost', user='root', password='',
                          database='news')  # подключим базу данных
    with con:
        cursor = con.cursor()
        data_list = (col1)
        cursor.execute("""INSERT INTO sentences (text_sentence) VALUES (%s);""", data_list)
        con.commit()
        cursor.close()


def check_sentence(text_sentence):
    # проверка предложения на наличие в базе
    con = pymysql.connect(host='localhost', user='root', password='',
                          database='news')  # подключим базу данных
    with con:
        cursor = con.cursor()
        cursor.execute("""SELECT text_sentence FROM sentences WHERE text_sentence = %s """, (text_sentence,))
        result = cursor.fetchall()
        if len(result) == 0:
            #print('[INFO] Такой записи нет')
            return 0
        else:
            print('[X] Такая запись существует')
            return 1


def get_data_from_db():
    # получение данных из бд
    con = pymysql.connect(host='localhost', user='root', password='',
                          database='news')  # подключим базу данных
    with con:
        cursor = con.cursor()
        cursor.execute("""SELECT text_sentence FROM sentences""")
        # вывод всех новостей
        data_set = cursor.fetchall()
        return data_set

if __name__ == '__main__':
    # основная часть кода
    # -------------------------------------
    # -------------------------------------

    # выгрузим все статьи
    # -------------------------------------

    headers = {
        'User-Agent': 'Mozilla/5.0 ',
        'Accept': '*/*'
    }

    '''
    url = 'file:/pretty.html'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    page = requests.get(url)
    print(page.status_code)
    '''
    os.system("start pretty.html")

    '''
    # забираем контент новостей перебирая ссылки
    count = 1
    while count < 71:
        url = 'file:///C:/Users/79616/Desktop/pretty.html'
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        #получим текст статьи

        text_sentence = soup.find('div', class_='entry-content').get_text(strip=True)

        # !!! дополнить полями из задания семы !!!

        print(f'Парсим в бд:\nПредложение: "{text_sentence}')
        count += 1

        # вставляем запись в бд
        try:
            insert_sentence()
            print('[INFO] Предложение добавлено в БД')
        except Exception as ex:
            print('[X] Ошибка вставки данных в бд: ', ex)
            #continue

        count += 1

    # вывод данных уже с созданной таблицы предложений бд
    data_set = get_data_from_db()
    for data in data_set:
        print(data)
    '''