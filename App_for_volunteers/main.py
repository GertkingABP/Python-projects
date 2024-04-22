import sqlite3

#-----------------------------------Cоединение с базой данных-----------------------------------#

conn = sqlite3.connect('db_for_volunteers.db')
cursor = conn.cursor()
print("Подключение к БД установлено.\n\n")

#-------------------------Работа с запросами к БД по выбору пользователя-------------------------#

flag_cycle = 0

while flag_cycle != 1:
    print("Выберите запрос, который хотите выполнить с БД для волонтёров:\n")
    print("1.Вывести первые N пожеланий волонтёров.")
    print("2.Вывести ФИО волонтёра, его роль и описание события, на которое он записан.")
    print("3.Добавить нового подопечного.")
    print("4.Обновить название роли вместо -.")
    print("5.Удалить пожелание по вхождению текста.")
    choice_querry = input("\n\nВаш выбор: ")

    if choice_querry == "1":
        N = int(input("\n\nВведите число N: "))
        cursor.execute("SELECT text_wish, datetime FROM wishes ORDER BY id_wish LIMIT '%d'" % N)
        result1 = cursor.fetchall()
        print("Результат запроса:\n", result1)

    elif choice_querry == "2":
        cursor.execute("select volunteers.full_name, roles.title_role, events.title from volunteers join roles on (volunteers.fk_id_role = roles.id_role) join events on (volunteers.fk_id_event = events.id_event) order by roles.title_role desc")
        result2 = cursor.fetchall()
        print("Результат запроса:\n", result2)

    elif choice_querry == "3":
        FIO = input("\n\nВведите ФИО подопечного: ")
        address = input("\n\nВведите адрес проживания подопечного: ")
        cursor.execute("INSERT INTO wards (name_ward, address) VALUES (?, ?)", (FIO, address))
        result3 = cursor.fetchall()
        conn.commit()
        cursor.execute("SELECT * FROM wards")
        result31 = cursor.fetchall()
        print("Результат запроса:\n", result31)

    elif choice_querry == "4":
        cursor.execute("UPDATE roles SET title_role = 'Комбинированная' WHERE (id_role AND title_role = '-')")
        result4 = cursor.fetchall()
        conn.commit()
        cursor.execute("SELECT * FROM roles")
        result41 = cursor.fetchall()
        print("Результат запроса:\n", result41)

    elif choice_querry == "5":
        text = input("\n\nВведите фрагмент пожелания: ")
        cursor.execute("DELETE FROM wishes WHERE text_wish LIKE '%s'" % text)
        result5 = cursor.fetchall()
        conn.commit()
        cursor.execute("SELECT * FROM wishes")
        result51 = cursor.fetchall()
        print("Результат запроса:\n", result51)

    else:
        print("Вы ввели что-то другое...\n")

    answer = input("\n\nХотите продолжить работу с запросами(1 - да, не 1 - нет)? ")
    if answer == "1":
        flag_cycle = 0

    elif answer != "1":
        print("Вы ответили нет.\n")
        flag_cycle = 1

#------------------------------Закрытие соединения с базой данных------------------------------#

conn.close()

