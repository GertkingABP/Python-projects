#import mysql.connector
import pymysql.cursors
import pymysql
import sys
import os

#ВСЕГО В БД 10016 НОВОСТЕЙ!
counter = 1
while counter < 480:
    result = 0
    lenltr = 0
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password="",
                                 db='news',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cur:
        try:
            cur.execute("select text_sentence from sentences where id_sentence = %d" %counter)
            result = cur.fetchmany(1)
            if result:
                newfile = open("sents.txt", "a+")
                newfile.write('' + "\n")

            for index in result:
                ltr = []
                ltr.append(index['text_sentence'])
                lenltr = len(ltr)
                for i in range(lenltr):
                    newfile.write('{}'.format(ltr[i]))
                    newfile.write("\t")
                    print(ltr[i])
                newfile.write("\n")
        except:
            print()

    connection.close()
    counter += 1
