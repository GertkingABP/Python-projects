#import mysql.connector
import pymysql.cursors
import pymysql
import sys
import os
from bs4 import BeautifulSoup

#ВСЕГО В БД 10016 НОВОСТЕЙ!
#НЕЛЬЗЯ ПЕРЕДАТЬ ВСЕ ТЕКСТЫ СРАЗУ В ТОМИТА-ПАРСЕР!

counter = 1
set_texts = 501
i1 = 1
while set_texts != 10501:
    while counter < set_texts:
        result = 0
        lenltr = 0
        connection = pymysql.connect(host='localhost',
                                     user='phpmyadmin',
                                     password="std",
                                     db='phpmyadmin',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cur:
            try:
                cur.execute("select content from news where id = %d" %counter)
                result = cur.fetchmany(1)
                if result:
                    os.chdir('/home/std/tomita-parser/build/bin')
                    newfile = open(f'contents{i1}.txt', "a+")
                    newfile.write('' + "\n")

                for index in result:
                    ltr = []
                    ltr.append(index['content'])
                    lenltr = len(ltr)
                    for i in range(lenltr):
                        newfile.write('{}'.format(ltr[i]))
                        newfile.write("\t")
                        print("Text #", counter, " ", ltr[i])
                    newfile.write("\n")

            except:
                #connection.rollback()
                print()

        connection.close()
        counter += 1
    set_texts += 500
    i1 += 1

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
            cur.execute("select content from news where id = %d" %counter)
            result = cur.fetchmany(1)
            if result:
                os.chdir('/home/std/tomita-parser/build/bin')
                newfile = open(f'contents{i1}.txt', "a+")
                newfile.write('' + "\n")

            for index in result:
                ltr = []
                ltr.append(index['content'])
                lenltr = len(ltr)
                for i in range(lenltr):
                    newfile.write('{}'.format(ltr[i]))
                    newfile.write("\t")
                    print("Text #", counter, " ", ltr[i])
                newfile.write("\n")

        except:
            #connection.rollback()
            print()

    connection.close()
    counter += 1

#os.chdir('/home/std/tomita-parser/build/bin')
#os.system('./tomita-parser config.proto')
