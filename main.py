import telebot
import sqlite3
import threading
from datetime import datetime

# Set up the bot
bot = telebot.TeleBot('5469451869:AAHC_8ar1tK2E_Vh9N_5rQtAEkZ9l3lhF0E')

# Connect to the SQLite database

#ДЛЯ АДМИНИТРАТОРА
conn = sqlite3.connect('lepta.db', check_same_thread=False)
cursor = conn.cursor()

# Create the user table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        status TEXT
    )
''')
conn.commit()

#ДЛЯ ВОЛОНТЁРА
conn1 = sqlite3.connect('db_for_volunteers.db', check_same_thread=False)
cursor1 = conn1.cursor()


# Store the user's status and username
user_status = {}
user_username = {}


# Handler for the "/start" command
@bot.message_handler(commands=['start'])
def start(message):
    # Send a welcome message and the status selection keyboard
    bot.reply_to(message, 'Добро пожаловать в телеграмм-бот волонтерского движения "Лепта".'
                          'Немного о нас:Братья и сестры из "Лепты" - это команда неравнодушных христиан, которые пытаются немного скрасить будни тех, кто нуждается в поддержке, привнеся в них радость, светлую радость о Боге и надежду на Него. Так случилось, что мы обнаружили в себе талант, которым владеем, и решили именно им послужить Богу и людям. Наше волонтерство и миссия опосредованы музыкой, поэтому взаимно отрадны и слушателям, и нам самим. Ежемесячно мы собираемся, чтобы прийти или в хоспис, или в интернат. Есть также мастерская "Конкордия", где добрые мастера помогают подготовиться к ярмарке. Периодически, участвуя в ярмарках, мы собираем средства на помощь хоспису и интернату, и другие дела благотворительности. С хосписом мы сотрудничаем около пяти лет. Хоспис - это чаще всего последнее пристанище для тяжело больных людей. Интернат - это пристанище для пожилых, которые нуждаются в медицинском уходе, и инвалидов, за которыми некому или тяжело ухаживать в миру. Среди инвалидов не мало молодых. Легко ли такое служение? На первый взгляд, ничего хитрого: что может быть легче того, что умеешь? Но с другой стороны, видя глаза и печали тех, кому ты все это адресуешь, ты чувствуешь, что не в состоянии помочь бОльшим. И единственно верным может быть понимание того, что Господь и не требует от нас этого бОльшего, потому что остальное - это Его вотчина. И значимы здесь только наши сердца, открытые зову Господа, Который нас сюда и привел. Если вы обладаете той лептой, которой можете помочь, присоединяйтесь. Вас ждут там!\n'
                          '\nНаш телеграмм-бот предназначен для взаимодействия с волонтерами, организациями и администраторами. Для продолжения нажмите на статус, который вам необходим:', reply_markup=get_status_keyboard())



# Handler for status selection
@bot.message_handler(func=lambda message: True and message.from_user.username not in user_username)
def handle_status(message):
    if message.text == 'Exit':
        handle_exit(message)
        return

    username = message.from_user.username

    status = message.text

    # Check if the selected status is valid
    if status in ['administrator', 'volunteer']:
        if status == 'administrator':
            # Ask for password
            bot.reply_to(message, 'Please enter the password for administrator access:')
        else:
            # Insert the user into the database in a separate thread
            threading.Thread(target=insert_user, args=(username, status)).start()

            # Send the exit button
            bot.reply_to(message, 'You have selected "{}" status.'.format(status), reply_markup=get_exit_volunteer_keyboard())

        # Store the user's status and username
        user_status[username] = status
        user_username[username] = username
    else:
        bot.reply_to(message, 'Invalid status. Please select a valid status.')


# Handler for password input
@bot.message_handler(func=lambda message: message.text != 'Exit' and message.from_user.username in user_username and user_status[message.from_user.username] == 'administrator' and not user_exists(message.from_user.username, 'administrator'))
def handle_password(message):
    username = message.from_user.username

    # Check if the entered password is correct
    if message.text == 'lepta':
        # Insert the user into the database in a separate thread
        threading.Thread(target=insert_user, args=(username, 'administrator')).start()

        # Send the exit button
        bot.reply_to(message, 'You have successfully logged in as an administrator.', reply_markup=get_exit_keyboard())
    else:
        bot.reply_to(message, 'Incorrect password. Please try again or go back to the status selection.')


# Handler for the exit button
@bot.message_handler(func=lambda message: message.text == 'Exit')
def handle_exit(message):
    username = message.from_user.username

    # Delete the user record from the database in a separate thread
    threading.Thread(target=delete_user, args=(username,)).start()

    # Reset the user's status and username
    del user_status[username]
    del user_username[username]

    # Send a confirmation message and the status selection keyboard
    bot.reply_to(message, 'Your record has been deleted. Please select your status:', reply_markup=get_status_keyboard())


# Handler for "analytical request1" button
@bot.message_handler(func=lambda message: message.text == 'Запрос 1' and message.from_user.username in user_username)

def handle_request1(message):
    # Handle the request to delete a volunteer
    username = message.from_user.username
    status = user_status[username]
    bot.reply_to(message,
                 'Выполняется аналитический запрос #1 к базе данных для пользователя "{}" со статусом "{}".'.format(
                     username, status))
    bot.reply_to(message,
                 'Суть запроса: Показать всех людей, которых ходят на ту или иную евангельскую группу.')

    # Get the list of all volunteers' names
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT name FROM evangelical_group')
    volunteer_names = select_cursor.fetchall()

    if len(volunteer_names) == 0:
        bot.reply_to(message, 'В базе данных отсутствуют типы евангельских групп.')
        return

    # Format the list of names as a string
    names_string = '\n'.join([name[0] for name in volunteer_names])
    bot.reply_to(message, f'Список евангельских групп:\n{names_string}')

    # Prompt the user to select a volunteer to delete
    bot.reply_to(message, 'Введите название евангельской группы, список которой хотите получить:')
    bot.register_next_step_handler(message, request1)

def request1(message):
    # Handle the analytical request 1
    username = message.from_user.username
    status = user_status[username]
    eg_name = message.text
    select_cursor = conn.cursor()
    select_cursor.execute('''
    SELECT v.name
    FROM volunteer v
    JOIN evangelical_group eg ON v.id_evangelical_group = eg.id
    WHERE eg.name = ?
    ''', (eg_name,))
    string1 = str(select_cursor.fetchall())
    bot.reply_to(message, f"Результат запроса: {string1}")


# Handler for "analytical request2" button
@bot.message_handler(func=lambda message: message.text == 'Запрос 2' and message.from_user.username in user_username)

def handle_request2(message):
    # Handle the request to delete a volunteer
    username = message.from_user.username
    status = user_status[username]
    bot.reply_to(message,
                 'Выполняется аналитический запрос #2 к базе данных для пользователя "{}" со статусом "{}".'.format(
                     username, status))
    bot.reply_to(message,
                 'Вывести общее кол-во волонтёров одной и той же роли и являющихся мужчинами. Укажите роль')

    # Get the list of all volunteers' names
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT title FROM roles')
    volunteer_names = select_cursor.fetchall()

    if len(volunteer_names) == 0:
        bot.reply_to(message, 'В базе данных отсутствуют типы ролей.')
        return

    # Format the list of names as a string
    names_string = '\n'.join([name[0] for name in volunteer_names])
    bot.reply_to(message, f'Список доступных ролей:\n{names_string}')

    # Prompt the user to select a volunteer to delete
    bot.reply_to(message, 'Введите название роли, список которой хотите получить:')
    bot.register_next_step_handler(message, request2)

def request2(message):
    # Handle the analytical request 1
    username = message.from_user.username
    status = user_status[username]
    role = message.text
    select_cursor = conn.cursor()
    select_cursor.execute('''
        SELECT COUNT(*) AS total_count
        FROM volunteer v
        JOIN roles r ON v.id_role = r.id
        WHERE v.sex = 'муж' AND r.title = ?
    ''', (role,))
    # print(f"Результат запроса: {select_cursor.fetchall()}")
    string1 = str(select_cursor.fetchall())
    bot.reply_to(message, f"Результат запроса: {string1}")


@bot.message_handler(func=lambda message: message.text == 'Получить информацию о волонтере' and
                                          message.from_user.username in user_username and
                                          user_status[message.from_user.username] == 'administrator')
def handle_search_volunteer(message):
    # Handle the request to delete a volunteer
    username = message.from_user.username
    status = user_status[username]

    bot.reply_to(message, 'Эта функция позволяет получить всю информацию о выбранном волонтере.')

    # Get the list of all volunteers' names
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT name FROM volunteer')
    volunteer_names = select_cursor.fetchall()

    if len(volunteer_names) == 0:
        bot.reply_to(message, 'В базе данных отсутствуют волонтеры.')
        return

    # Format the list of names as a string
    names_string = '\n'.join([name[0] for name in volunteer_names])
    bot.reply_to(message, f'Список волонтеров:\n{names_string}')

    # Prompt the user to select a volunteer to delete
    bot.reply_to(message, 'Введите имя волонтера, о котором хотите всё узнать:')
    bot.register_next_step_handler(message, search_volunteer)

def search_volunteer(message):
    volunteer_name = message.text

    # Check if the volunteer exists
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT name FROM volunteer WHERE name = ?', (volunteer_name,))
    volunteer = select_cursor.fetchone()

    if volunteer is None:
        bot.reply_to(message, 'Выбранный волонтер не найден. Повторите ввод.')
        return

    # Delete the volunteer from the database
    search_cursor = conn.cursor()
    search_cursor.execute('''
    SELECT 
  CASE 
    WHEN v.id_evangelical_group = eg.id THEN eg.name
    ELSE 'Нет евангельской группы'
  END AS 'Название группы',
  CASE
    WHEN v.id_role = r.id THEN r.title
    ELSE 'Нет роли'
  END AS 'Название роли',
  v.name,
  v.age,
  v.religion,
  v.sex,
  v.phone_number
FROM volunteer v
LEFT JOIN evangelical_group eg ON v.id_evangelical_group = eg.id
LEFT JOIN roles r ON v.id_role = r.id
WHERE v.name = ?
    ''', (volunteer_name,))
    conn.commit()

    string1 = str(search_cursor.fetchall())
    bot.reply_to(message, f"Результат запроса: {string1}")

@bot.message_handler(func=lambda message: message.text == 'Удалить волонтера' and
                                          message.from_user.username in user_username and
                                          user_status[message.from_user.username] == 'administrator')
def handle_delete_volunteer(message):
    # Handle the request to delete a volunteer
    username = message.from_user.username
    status = user_status[username]

    bot.reply_to(message, 'Эта функция позволяет удалить выбранного волонтера.')

    # Get the list of all volunteers' names
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT name FROM volunteer')
    volunteer_names = select_cursor.fetchall()

    if len(volunteer_names) == 0:
        bot.reply_to(message, 'В базе данных отсутствуют волонтеры.')
        return

    # Format the list of names as a string
    names_string = '\n'.join([name[0] for name in volunteer_names])
    bot.reply_to(message, f'Список волонтеров:\n{names_string}')

    # Prompt the user to select a volunteer to delete
    bot.reply_to(message, 'Введите имя волонтера, которого нужно удалить:')
    bot.register_next_step_handler(message, delete_volunteer)

def delete_volunteer(message):
    volunteer_name = message.text

    # Check if the volunteer exists
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT name FROM volunteer WHERE name = ?', (volunteer_name,))
    volunteer = select_cursor.fetchone()

    if volunteer is None:
        bot.reply_to(message, 'Выбранный волонтер не найден. Повторите ввод.')
        return

    # Delete the volunteer from the database
    delete_cursor = conn.cursor()
    delete_cursor.execute('DELETE FROM volunteer WHERE name = ?', (volunteer_name,))
    conn.commit()

    bot.reply_to(message, f'Волонтер {volunteer_name} успешно удален из базы данных!')



@bot.message_handler(func=lambda message: message.text == 'Изменить роль волонтера' and
                                          message.from_user.username in user_username and
                                          user_status[message.from_user.username] == 'administrator')
def handle_update_role(message):
    # Handle the request to update volunteer role
    username = message.from_user.username
    status = user_status[username]

    bot.reply_to(message, 'Эта функция позволяет обновить роль выбранного волонтера.')

    # Get the list of all volunteers' names
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT name FROM volunteer')
    volunteer_names = select_cursor.fetchall()

    if len(volunteer_names) == 0:
        bot.reply_to(message, 'В базе данных отсутствуют волонтеры.')
        return

    # Format the list of names as a string
    names_string = '\n'.join([name[0] for name in volunteer_names])
    bot.reply_to(message, f'Список волонтеров:\n{names_string}')

    # Get the list of all roles with their ids
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT id, title FROM roles')
    roles = select_cursor.fetchall()

    if len(roles) == 0:
        bot.reply_to(message, 'В базе данных отсутствуют роли.')
        return

    # Format the list of roles with ids as a string
    roles_string = '\n'.join([f"{role[0]} - {role[1]}" for role in roles])
    bot.reply_to(message, f'Список доступных ролей:\n{roles_string}')

    # Prompt the user to select a volunteer
    bot.reply_to(message, 'Введите имя волонтера, роль которого нужно обновить:')
    bot.register_next_step_handler(message, update_volunteer_role)

def update_volunteer_role(message):
    volunteer_name = message.text

    # Check if the volunteer exists
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT name FROM volunteer WHERE name = ?', (volunteer_name,))
    volunteer = select_cursor.fetchone()

    if volunteer is None:
        bot.reply_to(message, 'Выбранный волонтер не найден. Повторите ввод.')
        return

    # Prompt the user to enter the new role
    bot.reply_to(message, 'Введите id роли(их список представлен выше) для волонтера:')
    bot.register_next_step_handler(message, process_updated_role, volunteer_name)

def process_updated_role(message, volunteer_name):
    new_role = message.text

    # Update the volunteer's role in the database
    update_cursor = conn.cursor()
    update_cursor.execute('UPDATE volunteer SET id_role = ? WHERE name = ?', (new_role, volunteer_name))
    conn.commit()

    bot.reply_to(message, f'Роль волонтера {volunteer_name} успешно обновлена на {new_role}!')


# глобальные переменные для записи волонтера
id_role = None
id_evangelical_group = None
phone_number = None
sex = None
religion = None
age = None

@bot.message_handler(func=lambda message: message.text == 'Добавить волонтера в базу' and
                                          message.from_user.username in user_username and
                                          user_status[message.from_user.username] == 'administrator')
def handle_insert_volunteer(message):
    # Handle the analytical request 1
    username = message.from_user.username
    status = user_status[username]

    bot.reply_to(message, 'Эта функция позволяет добавить указанного волонтера в базу данных. Напишите любое сообщение, чтобы продолжить')

    # Ввод данных
    bot.register_next_step_handler(message, ask_id_role)

def ask_id_role(message):
    bot.reply_to(message, 'Введите id_role:')
    bot.register_next_step_handler(message, ask_id_evangelical_group)

def ask_id_evangelical_group(message):
    global id_role
    id_role = message.text
    bot.reply_to(message, 'Введите id_evangelical_group:')
    bot.register_next_step_handler(message, ask_phone_number)

def ask_phone_number(message):
    global id_evangelical_group
    id_evangelical_group = message.text
    bot.reply_to(message, 'Введите phone_number:')
    bot.register_next_step_handler(message, ask_sex)

def ask_sex(message):
    global phone_number
    phone_number = message.text
    bot.reply_to(message, 'Введите sex:')
    bot.register_next_step_handler(message, ask_religion)

def ask_religion(message):
    global sex
    sex = message.text
    bot.reply_to(message, 'Введите religion:')
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    global religion
    religion = message.text
    bot.reply_to(message, 'Введите age:')
    bot.register_next_step_handler(message, ask_name)

def ask_name(message):
    global age
    age = message.text
    bot.reply_to(message, 'Введите name:')
    bot.register_next_step_handler(message, save_volunteer)

def save_volunteer(message):
    name = message.text

    try:
        # Занесение данных в таблицу
        insert_cursor = conn.cursor()
        insert_cursor.execute('''
        INSERT INTO volunteer (
                              id_role,
                              id_evangelical_group,
                              phone_number,
                              sex,
                              religion,
                              age,
                              name
                          )
                          VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (int(id_role), int(id_evangelical_group), phone_number, sex, religion, int(age), name))
        conn.commit()

        bot.reply_to(message, 'Волонтер с указанными данными добавлен!')

    except Exception as e:
        # Handle the error
        error_message = f'Ошибка при добавлении волонтера: {str(e)}. Введите данные заново и корректно!'
        bot.reply_to(message, error_message)


# прочие функции
# Helper function to insert a user into the database
def insert_user(username, status):
    insert_cursor = conn.cursor()
    insert_cursor.execute('INSERT INTO users (name, status) VALUES (?, ?)', (username, status))
    conn.commit()


# Helper function to delete a user from the database
def delete_user(username):
    delete_cursor = conn.cursor()
    delete_cursor.execute('DELETE FROM users WHERE name=?', (username,))
    conn.commit()


# Helper function to create the status selection keyboard
def get_status_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('administrator', 'volunteer')
    return keyboard


# Helper function to create the exit button keyboard
def get_exit_keyboard():#ДЛЯ АДМИНИСТРАТОРА
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Exit', 'Запрос 1', 'Запрос 2', 'Добавить волонтера в базу', "Изменить роль волонтера", "Удалить волонтера", "Получить информацию о волонтере")
    return keyboard

def get_exit_volunteer_keyboard(): #ДЛЯ ПРОФИЛЯ ВОЛОНТЁРА
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Exit', 'Узнать свои мероприятия и роли на каждом', 'Проверить свои данные', 'Показать всех своих подопечных и их данные', 'Добавить пожелание')
    return keyboard

# Helper function to check if a user with a specific status exists in the database
def user_exists(username, status):
    select_cursor = conn.cursor()
    select_cursor.execute('SELECT * FROM users WHERE name=? AND status=?', (username, status))
    return select_cursor.fetchone() is not None

#-------------------------------------------ФУНКЦИИ ДЛЯ ПРОФИЛЯ ВОЛОНТЁРА-------------------------------------------#

#---------------------------------------------------------------------#
#ПЕРВЫЙ ЗАПРОС ВОЛОНТЁРА
@bot.message_handler(func=lambda message: message.text == 'Узнать свои мероприятия и роли на каждом' and
                                          message.from_user.username in user_username and
                                          user_status[message.from_user.username] == 'volunteer')
def first_select_for_volunteer(message):
    username1 = message.from_user.username
    status1 = user_status[username1]
    bot.reply_to(message,
                 'Выполняется аналитический запрос #1 к базе данных волонтёров для волонтёра "{}" со статусом "{}".'.format(
                     username1, status1))
    bot.reply_to(message,
                 'Суть запроса: Показать название и дату мероприятия с ролью данного пользователя/волонтёра.')

    select_cursor1 = conn1.cursor()
    select_cursor1.execute('''select volunteers.full_name,
                           roles.title_role,
                           events.title,
                           events.datetime from volunteers 
                           join roles on (volunteers.fk_id_role = roles.id_role) 
                           join events on (volunteers.fk_id_event = events.id_event) WHERE volunteers.full_name = ? order by roles.title_role desc;''', (username1,))
    conn1.commit()

    answer_1 = select_cursor1.fetchall()

    if len(answer_1) == 0:
        bot.reply_to(message, 'В базе данных ничего не найдено.')
        return

    string_1 = str(answer_1)
    bot.reply_to(message, f"Результат запроса: {string_1}")

#---------------------------------------------------------------------#
#ВТОРОЙ ЗАПРОС ВОЛОНТЁРА
@bot.message_handler(func=lambda message: message.text == 'Проверить свои данные' and
                                          message.from_user.username in user_username and
                                          user_status[message.from_user.username] == 'volunteer')
def second_select_for_volunteer(message):
    username2 = message.from_user.username
    status2 = user_status[username2]
    bot.reply_to(message,
                 'Выполняется аналитический запрос #2 к базе данных волонтёров для волонтёра "{}" со статусом "{}".'.format(
                     username2, status2))
    bot.reply_to(message,
                 'Суть запроса: Показать текущие данные пользователя/волонтёра.')

    select_cursor2 = conn1.cursor()
    select_cursor2.execute('''select full_name, age, phone_number from volunteers
                           where full_name = ?''',
                           (username2,))
    conn1.commit()

    answer_2 = select_cursor2.fetchone()

    if len(answer_2) == 0:
        bot.reply_to(message, 'В базе данных ничего не найдено. Возможно, вас ещё не добавили в качестве волонтёра.')
        return

    string_2 = str(answer_2)
    bot.reply_to(message, f"Ваши текущие данные: {string_2}")
    bot.reply_to(message, "Если в данных содержится ошибка или что-то из данных не актуально, то обратитесь к администратору.")

#---------------------------------------------------------------------#
#ТРЕТИЙ ЗАПРОС ВОЛОНТЁРА
@bot.message_handler(func=lambda message: message.text == 'Показать всех своих подопечных и их данные' and
                                          message.from_user.username in user_username and
                                          user_status[message.from_user.username] == 'volunteer')
def third_select_for_volunteer(message):
    username3 = message.from_user.username
    status3 = user_status[username3]
    bot.reply_to(message,
                 'Выполняется аналитический запрос #3 к базе данных волонтёров для волонтёра "{}" со статусом "{}".'.format(
                     username3, status3))
    bot.reply_to(message,
                 'Суть запроса: Показать данные о подопечных данного пользователя/волонтёра.')

    select_cursor3 = conn1.cursor()
    select_cursor3.execute('''select volunteers.full_name, 
                           wards.name_ward, 
                           wards.address 
                           from volunteers 
                           join volunteers_to_wards on (volunteers_to_wards.fk_id_volunteer = volunteers.id_volunteer) 
                           join wards on (volunteers_to_wards.fk_id_ward = wards.id_ward) where volunteers.full_name = ?''',
                           (username3,))
    conn1.commit()

    answer_3 = select_cursor3.fetchall()

    if len(answer_3) == 0:
        bot.reply_to(message,
                     'В базе данных ничего не найдено. Возможно, что для вас ещё не подобрали подопечных или вас ещё не добавили в качестве волонтёра.')
        return

    string_3 = str(answer_3)
    bot.reply_to(message, f"У вас следующие подопечные: {string_3}")

#---------------------------------------------------------------------#
# ДОБАВИТЬ ПОЖЕЛАНИЕ ВОЛОНТЁРА
@bot.message_handler(func=lambda message: message.text == 'Добавить пожелание' and
                                          message.from_user.username in user_username and
                                          user_status[message.from_user.username] == 'volunteer')
def ask_text_wish(message):
    bot.reply_to(message, 'Эта функция позволяет добавить ваше пожелание в базу данных.')
    username4 = message.from_user.username
    status4 = user_status[username4]
    global text_wish
    text_wish = ''
    bot.reply_to(message, 'Введите text_wish:')
    bot.register_next_step_handler(message, save_wish)


def save_wish(message):
    username4 = message.from_user.username
    status4 = user_status[username4]
    now_datetime = datetime.now()
    date_time_str = now_datetime.strftime("%Y-%m-%d %H:%M:%S")
    select4_cursor = conn1.cursor()
    select4_cursor.execute('SELECT id_volunteer FROM volunteers WHERE full_name = ?', (username4,))
    volunteer_id = select4_cursor.fetchone()

    if volunteer_id is None:
        bot.reply_to(message, 'Вы не можете добавить пожелание, поскольку вас нет в базе данных.')
        return

    string_id = str(volunteer_id[0])
    try:
        # Получение значения текста пожелания из переменной text_wish
        global text_wish
        text_wish = message.text

        # Занесение данных в таблицу
        insert_wish_cursor = conn1.cursor()
        insert_wish_cursor.execute('''
        INSERT INTO wishes (
                              text_wish,
                              datetime,
                              fk_id_volunteer
                          )
                          VALUES (?, ?, ?)
        ''', (text_wish, date_time_str, string_id,))
        conn1.commit()

        bot.reply_to(message, 'Ваше пожелание с указанными данными добавлено!')

    except Exception as e:
        # Handle the error
        error_message = f'Ошибка при добавлении пожелания: {str(e)}. Введите данные заново и корректно!'
        bot.reply_to(message, error_message)
#------------------------------------------------------------------------------------------------------------------#

# Start the bot
bot.polling()
