--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.3 в Пт мар 10 00:25:33 2023
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: events
CREATE TABLE IF NOT EXISTS events (id_event integer not null primary key autoincrement, title text not null, datetime text not null, fk_id_type references types_event(id_type), fk_id_status references statuses_events(id_status));
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (1, 'Поздравление ветеранов', '02.02.2023 9.00', 3, 3);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (2, 'Помощь беженцам Донбасса', '05.02.2023 10.00', 6, 3);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (3, 'Открытие кружка', '08.02.2023 12.00', 10, 3);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (4, 'Помощь в пожертвовании вещей детям интерната', '09.02.2023 11.30', 9, 3);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (5, 'Слушание службы в монастыре', '11.02.2023 8.30', 2, 3);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (6, 'Уборка территории детского сада', '13.02.2023 10.00', 1, 2);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (7, 'Сбор средств для пенсионеров хосписа', '13.02.2023 14.00', 7, 3);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (8, 'Уборка территории храма', '15.02.2023 9.35', 2, 3);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (9, 'Совместное чтение Евангелие и музыкальные выступления', '16.02.2023 12.00', 10, 2);
INSERT INTO events (id_event, title, datetime, fk_id_type, fk_id_status) VALUES (10, 'Выступление группы молодёжного отдела', '15.02.2023 15.00', 8, 3);

-- Таблица: roles
CREATE TABLE IF NOT EXISTS roles (id_role integer not null primary key autoincrement, title_role text not null);
INSERT INTO roles (id_role, title_role) VALUES (1, 'Администратор');
INSERT INTO roles (id_role, title_role) VALUES (2, 'Водитель');
INSERT INTO roles (id_role, title_role) VALUES (3, 'Певец');
INSERT INTO roles (id_role, title_role) VALUES (4, 'Гитарист');
INSERT INTO roles (id_role, title_role) VALUES (5, 'Скрипач');
INSERT INTO roles (id_role, title_role) VALUES (6, 'Фронт-мен');
INSERT INTO roles (id_role, title_role) VALUES (7, 'Организатор');
INSERT INTO roles (id_role, title_role) VALUES (8, 'Меценат');
INSERT INTO roles (id_role, title_role) VALUES (9, 'Программист');
INSERT INTO roles (id_role, title_role) VALUES (10, 'Комбинированная');

-- Таблица: statuses_events
CREATE TABLE IF NOT EXISTS statuses_events (id_status integer not null primary key autoincrement, title_status text not null);
INSERT INTO statuses_events (id_status, title_status) VALUES (1, 'Запланированно');
INSERT INTO statuses_events (id_status, title_status) VALUES (2, 'Отменено');
INSERT INTO statuses_events (id_status, title_status) VALUES (3, 'Проведено');

-- Таблица: types_event
CREATE TABLE IF NOT EXISTS types_event (id_type integer not null primary key autoincrement, name_type text not null);
INSERT INTO types_event (id_type, name_type) VALUES (1, 'Экодесант');
INSERT INTO types_event (id_type, name_type) VALUES (2, 'Выезд в храм');
INSERT INTO types_event (id_type, name_type) VALUES (3, 'Выезд в хоспис');
INSERT INTO types_event (id_type, name_type) VALUES (4, 'Велоэкскурсия');
INSERT INTO types_event (id_type, name_type) VALUES (5, 'Паломничество');
INSERT INTO types_event (id_type, name_type) VALUES (6, 'Гуманитарная помощь');
INSERT INTO types_event (id_type, name_type) VALUES (7, 'Материальная помощь');
INSERT INTO types_event (id_type, name_type) VALUES (8, 'Отдых вместе');
INSERT INTO types_event (id_type, name_type) VALUES (9, 'Сбор вещей для детей');
INSERT INTO types_event (id_type, name_type) VALUES (10, 'Евангельский кружок');

-- Таблица: volunteers
CREATE TABLE IF NOT EXISTS volunteers (id_volunteer integer not null primary key autoincrement, full_name text not null, age integer not null, phone_number text not null, evang_group text not null, fk_id_event references events(id_event), fk_id_role references roles(id_role));
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (1, 'Иванов Николай Петрович', 30, '89618479922', 'Взрослая', 1, 2);
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (2, 'Григорьев Алексей Иванович', 25, '89053334366', 'Не ходит', 1, 7);
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (3, 'Володин Владимир Владимирович', 19, '89043332211', 'Молодёжная', 1, 10);
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (4, 'Циханова Нина Анатольевна', 31, '89615559900', 'Взрослая', 2, 8);
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (5, 'Пенкин Влад Олегович', 43, '89610039438', 'Взрослая', 2, 9);
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (6, 'Романова Евгения Романовна', 33, '89045835522', 'Не ходит', 2, 7);
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (7, 'Алёхина Александра Павловна', 21, '89178885332', 'Молодёжная', 3, 10);
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (8, 'Павлов Андрей Николаевич', 18, '89615554433', 'Молодёжная', 3, 9);
INSERT INTO volunteers (id_volunteer, full_name, age, phone_number, evang_group, fk_id_event, fk_id_role) VALUES (9, 'Петров Николай Евгеньевич', 32, '89618778901', 'Не ходит', 3, 6);

-- Таблица: volunteers_to_wards
CREATE TABLE IF NOT EXISTS volunteers_to_wards(fk_id_volunteer references volunteers(id_volunteer), fk_id_ward references wards(id_ward), primary key (fk_id_volunteer, fk_id_ward));
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (1, 1);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (1, 4);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (2, 2);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (3, 10);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (4, 3);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (5, 6);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (6, 5);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (6, 8);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (7, 9);
INSERT INTO volunteers_to_wards (fk_id_volunteer, fk_id_ward) VALUES (8, 1);

-- Таблица: wards
CREATE TABLE IF NOT EXISTS wards(id_ward integer not null primary key autoincrement, name_ward text not null, address text not null);
INSERT INTO wards (id_ward, name_ward, address) VALUES (1, 'Никулин Никита Артёмович', 'Ул.64 Армии, д.25, кв.31');
INSERT INTO wards (id_ward, name_ward, address) VALUES (2, 'Володина Елена Романовна', 'Пр.Ленина, д.27, кв.14');
INSERT INTO wards (id_ward, name_ward, address) VALUES (3, 'Степанов Павел Петрович', 'Бульвар Энгельса, 3Б, кв.2');
INSERT INTO wards (id_ward, name_ward, address) VALUES (4, 'Фахитова Екатерина Михайловна', 'Ул.Николая Отрады, д.52');
INSERT INTO wards (id_ward, name_ward, address) VALUES (5, 'Зурина Полина Андреевна', 'Ул.62 Армии, д.33, кв.33');
INSERT INTO wards (id_ward, name_ward, address) VALUES (6, 'Шохин Олег Иванович', 'Пр.Металлургов, д.4А, кв.23');
INSERT INTO wards (id_ward, name_ward, address) VALUES (7, 'Сергеев Роман Николаевич', 'Ул.Аджарская, д.18, кв.77');
INSERT INTO wards (id_ward, name_ward, address) VALUES (8, 'Алексеев Алексей Алексеевич', '-');
INSERT INTO wards (id_ward, name_ward, address) VALUES (9, 'Корзинина Ангелина Андреевна', 'Пр.Ленина, д.13');
INSERT INTO wards (id_ward, name_ward, address) VALUES (10, 'Власов Владимир Владимирович', 'Улица Строителей, д.44');

-- Таблица: wishes
CREATE TABLE IF NOT EXISTS wishes(id_wish integer not null primary key autoincrement, text_wish text not null, datetime text not null, fk_id_volunteer references volunteers(id_volunteer));
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (1, 'Необходимо пополнить ряды гитаристов!', '04.02.2023 12:54', 1);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (2, 'Всё хорошо, но реставрация для храма по-прежнему необходима.', '03.02.2023 20:46', 2);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (3, 'Сильная нехватка выдаваемых продуктов для нуждающихся, при разделении иногда выходит так, что на многодетную семью выделено совсем немного еды.', '03.02.2023 22:22', 3);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (4, 'Хотелось бы создать новый кружок по обучению игре на музыкальных инструментах', '05.02.2023 12.16', 4);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (5, 'На экологические выезды выделяется недостаточное кол-во волонтёров, не всегда вовремя справляемся!', '05.02.2023 12.18', 1);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (6, 'Евангельский кружок следует проводить хотя бы раз в неделю.', '05.02.2023 15.35', 7);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (7, 'Все молодцы, главное - учитывать достижения волонтёров(если они есть).', '05.02.2023 15.46', 4);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (8, 'Всё прекрасно :) Только хотел бы увидеть обновление библиотеки по книгам', '08.02.2023 23.44', 1);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (9, 'Периодически сталкиваемся с проблемой нехватки людей на мероприятия, следует по-другому распределять людей.', '09.02.2023 10.11', 8);
INSERT INTO wishes (id_wish, text_wish, datetime, fk_id_volunteer) VALUES (10, 'Продуктов, конечно, хватает для многих, но иногда распределение не совсем хорошее.', '12.02.2023 17.18', 9);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
