import sender_stand_request

import data

import requests

def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body

def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    print("Код ответа после создания пользователя:", user_response.status_code)

    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""
    print("Поле authToken в ответе не пустое")

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1
    print("Пользователь присутствует в таблице пользователей и он единственный")

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")
    assert False

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")
    assert False

def negative_assert_symbol(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)

    # В переменную response сохраняется результат запроса
    response = sender_stand_request.post_new_user(user_body)

    # Проверка, что код ответа равен 400
    assert response.status_code == 400
    print("Код ответа после отправки некорректного запроса:", response.status_code)

    # Проверка, что в теле ответа атрибут "code" равен 400
    assert response.json()["code"] == 400
    print("Атрибут 'code' в теле ответа равен 400")

    # Проверка текста в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"
    print("Сообщение об ошибке соответствует ожидаемому")