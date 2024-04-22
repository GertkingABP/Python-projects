
import pymysql.cursors
import pymysql
import sys
import os
import bs4
from bs4 import BeautifulSoup
import requests

#import mysql.connector
import pymysql.cursors
import pymysql
import sys
import os
from bs4 import BeautifulSoup

#ВСЕГО В БД 10016 НОВОСТЕЙ!
'''
counter = 1
while counter < 10017:
    result = 0
    lenltr = 0
    connection = pymysql.connect(host='localhost',
                                 user='phpmyadmin',
                                 password="std",
                                 db='phpmyadmin',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cur:
        try:
            sent = ''
            with open('facts1.txt.', 'r') as file:
                t = file.read
                soup = BeautifulSoup(t, 'html.parser')
                all_a = soup.find("table").find_all("a")
                for i in all_a:
                    sent += i.text
            with connection.cursor() as cur1:
                sql = """insert into sentences (text_sent) values (%s)"""  \
                        %(sent)
                cur1.execute(sql)
                connection.commit()

                #cur.execute("insert into sentences (text_sent) values (%s)" %sent)
                #print("Предложение", str(sent))

        except:
            connection.rollback()
            print()

    connection.close()
    counter += 1
'''

connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password="",
                                 db='news',
                                 cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cur:
    try:
        sent = ''
        with os.open('facts1.txt.', 'r') as file:
            t = file.read()
            soup = BeautifulSoup(t, 'html.parser')
            all_a = soup.find("table").find_all("Person")
            for i in all_a:
                sent += i.text
        with connection.cursor() as cur1:
            sql = """insert into sentences (text_sentence) values (%s)""" %(sent)
            cur1.execute(sql)
            connection.commit()

            #cur.execute("insert into sentences (text_sent) values (%s)" %sent)
            #connection.commit()
            #print("Предложение", str(sent))

    except:
        connection.rollback()
        print()

connection.close()

'''
response = requests.get("C:/OpenServer/domains/komp/sent1.html")
print(response.status_code)
'''