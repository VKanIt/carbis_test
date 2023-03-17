from dadata import Dadata
import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'users_dadata.db')

url="https://dadata.ru/"

errors={
    100:'Ошибка: Неверное имя пользователя или пароль!',
    101:'Ошибка: Данное имя пользователя уже существует!',
    102:'Ошибка: Команда не найдена!',
    103:'Ошибка: Не удалось подключиться к БД!',
    104:'Ошибка: Номер в списке не найден!',
    105:'Ошибка: Адрес не введен!'
}

try:
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    while True:
        print("У вас есть авторизация?")
        print("     Если да, введите 1")
        print("     Если нет, введите 2")
        print("     Если хотите выйти, введите exit")
        auth = input(">> ")
        
        if auth == '1':
            print("----------------------------")
            name = input("Имя пользователя: ")
            password = input("Пароль: ")
            sqlite_select_query = "select apikey,language from users where name = '" + name + "' and password = '" + password + "';"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            if not record:
                print("\n",errors[100],"\n")
            else:
                token = record[0][0]
                language = record[0][1]
                print("\nВход выполнен!")
                print("Язык на котором будет возвращен ответ: ", language,"\n")
                break
        elif auth == '2':
            print("----------------------------")
            name = input("Задайте имя пользователя: ")
            sqlite_select_query = "select name from users where name = '" + name + "';"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            if not record:
                password = input("Задайте пароль: ")
                token = input("API-ключ: ")
                print("На каком языке возвращать ответ (по умолчанию русский)?")
                print("     Если на английском (en), введите 1")
                print("     Пропустить нажмите Enter")
                language = input(">> ")
                if language != "1" and language != "":
                    print("\n",errors[102],"\n")
                else:
                    if language == "":
                        lg = "ru"
                    elif language == "1":
                        lg = "en"
                    sqlite_insert_query = "INSERT INTO users (name,password,url,apikey,language) VALUES ('" + name + "','" + password + "','" + url + "','" + token + "','" + lg + "');"
                    cursor.execute(sqlite_insert_query)
                    conn.commit()
                    print("\nПользователь создан!\n")
                    break 
            else:
                print("\n",errors[101],"\n")
        elif auth == 'exit':
            print("\nПрограмма завершена!")
            exit()
        else:
            print("\n",errors[102],"\n")
    cursor.close()
    conn.close()
except sqlite3.Error as error:
    print("\n",errors[103], error,"\n")

query=""
while True:
    print("----------------------------")
    dadata = Dadata(token)
    query=input("Введите адрес (для выхода введите 'exit')\n>> ")
    if query == "exit":
        dadata.close()
        print("\nПрограмма завершена!")
        break
    elif query == "":
        print("\n",errors[105],"\n")
    else:
        addresses = dadata.suggest("address", query, count = 20, language=language)
        print("----------------------------")
        print_address=list()
        for i in range(0,len(addresses)):
            print(i, ". ", addresses[i].get('unrestricted_value'), sep="")
            print_address.append(addresses[i].get('unrestricted_value'))
    
        print("\n----------------------------")
        print("Адрес находится в списке?")
        print("     Если да, введите 1")
        print("     Если нет, введите 2")
        print("     Если хотите выйти, введите exit")
        addressInList = input(">> ")
        print("\n----------------------------")
        if addressInList == '1':
            while True:
                try:
                    id_address = input("Введите номер адреса из предложенных вариантов\n>> ")
                    geo_coord = dadata.suggest("address", print_address[int(id_address)], count = 1, language=language)
                    print("Координаты широты: ", geo_coord[0].get('data').get('geo_lat'))
                    print("Координаты долготы: ", geo_coord[0].get('data').get('geo_lon'))
                    break
                except:
                    print("\n",errors[104],"\n")
        elif addressInList == '2':
            print("\nВведите более точный адрес!\n")
        elif addressInList == 'exit':
            print("\nПрограмма завершена!")
            break
        else:
            print("\n",errors[102],"\n")
    dadata.close()
