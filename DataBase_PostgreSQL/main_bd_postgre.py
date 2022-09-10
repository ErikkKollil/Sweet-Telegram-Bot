import psycopg2
from datetime import datetime
from DataBase_PostgreSQL.config_postgre import host, user, password, db_name

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.set_client_encoding('UTF8')
    connection.autocommit = True  # Авто_коммит
    print('[INFO+] DB is connect!')
except Exception as e:
    print('[GLOBAL_INFO_ERROR-]:', e)


# Создание или проверка таблицы prod
def creat_table_contact():
    with connection.cursor() as cursor:
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS contact(
                                contact_numid SERIAL NOT NULL PRIMARY KEY, 
                                contact_userid INTEGER NOT NULL,
                                contact_name TEXT NOT NULL CHECK (LENGTH(contact_name) > 1),
                                contact_number TEXT NOT NULL CHECK (LENGTH(contact_number) > 1),
                                contact_date timestamp NOT NULL);""")
            # conn.commit()
            print('[INFO+] Successfully validated table contact!')
        except Exception as e:
            print(e)
            print('[INFO-] Failed to create contact table!')


# Создание или проверка таблицы prod
def creat_table_reviews():
    with connection.cursor() as cursor:
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS reviews(
               reviews_id SERIAL NOT NULL PRIMARY KEY,
               reviews_userid INTEGER NOT NULL,
               reviews_firstname TEXT NOT NULL CHECK (LENGTH(reviews_firstname) > 1),
               reviews_username TEXT NOT NULL CHECK (LENGTH(reviews_username) > 1),
               reviews_name TEXT NOT NULL CHECK (LENGTH(reviews_name) > 1),
               reviews_date timestamp NOT NULL,
               reviews_comment text NOT NULL);""")
            connection.commit()
            print('[INFO+] Reviews table successfully checked!')
        except Exception as e:
            print(e)
            print('[INFO-] Failed to create reviews table!')


# Вставка данных в талицу contact
def execute_contact(user_id, first_name, phone_number):
    with connection.cursor() as cursor:
        try:
            sql_request = "INSERT INTO contact (contact_userid, contact_name, contact_number, contact_date) VALUES('{0}', '{1}', '{2}', '{3}');"
            cursor.execute(sql_request.format
                           (user_id, first_name, phone_number, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            connection.commit()
            print("[INFO+] New values have been added to the contact table!")
        except Exception as e:
            print('[INFO-] An error occurred while checking contact elements for duplicates:')
            print(e)


# Вставка данных в таблицу reviews (comment)
def execute_comment(user_id, first_name, user_name, name, comment):
    with connection.cursor() as cursor:
        try:
            sql_request = "INSERT INTO reviews (reviews_userid, reviews_firstname, reviews_username, reviews_name, reviews_date, reviews_comment) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');"
            cursor.execute(sql_request.format
                           (user_id, first_name, user_name, name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), comment))
            connection.commit()
            print("[INFO+] New values have been added to the reviews table!")
        except Exception as e:
            print('[INFO-] An error occurred while checking reviews elements for duplicates:')
            print(e)


# Проверка на дубликаты в таблице
def checkin_contact(user_id):
    with connection.cursor() as cursor:
        date_now = datetime.today()
        answer = False  # Ставим, что до проверки одинаковых элементов нет
        try:
            sql_request = """SELECT contact_userid, contact_date FROM contact;"""
            cursor.execute(sql_request)  # Выполнить запрос
            all_results = cursor.fetchall()
            for i in range(0, len(all_results)):
                userid = all_results[i][0]
                date_save = all_results[i][1]
                if userid == user_id and (date_now - date_save).days < 10:
                    print('[INFO+] This element is already in the table!')
                    answer = True
                    return answer
                else:
                    continue
            return answer
        except Exception as e:
            print('[INFO-] An error occurred when elements were triggered for duplicates:')
            print(e)
