#import mysql.connector
import pymysql.cursors
import pymysql
import sys
import os
from bs4 import BeautifulSoup

#ВСЕГО В БД 10016 НОВОСТЕЙ!

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
            cur.execute("select content from news where id = %d" %counter)
            result = cur.fetchall()
            if result:
                newfile = open("/home/std/tomita-parser/build/bin/content_one.txt", "w")
                newfile.write('' + "\n")

            for index in result:
                ltr = []
                ltr.append(index['content'])
                lenltr = len(ltr)
                for i in range(lenltr):
                    newfile.write('{}'.format(ltr[i]))
                    newfile.write("\t")
                    print(ltr[i])
                newfile.write("\n")
            os.chdir('/home/std/tomita-parser/build/bin')
            open('/home/std/tomita-parser/build/bin/pretty.html', 'w').close()
            os.system('./tomita-parser config.proto')
            sent = ''
            with open('/home/std/tomita-parser/build/bin/pretty.html', 'r') as file:
                html = file.read
                soup = BeautifulSoup(html, 'html.parser')
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
