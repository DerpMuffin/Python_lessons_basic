
""" 
== OpenWeatherMap ==

OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.

Необходимо решить следующие задачи:

== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.
    
    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID, 
    используя дополнительную библиотеку GRAB (pip install grab)

        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up

        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in

        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys
        
        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

        
== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz
    
    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка 
     (воспользоваться модулем gzip 
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)
    
    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}
== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a

    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a

    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a


    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}    


== Сохранение данных в локальную БД ==    
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):

    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных

2. Выводить список стран из файла и предлагать пользователю выбрать страну 
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))

3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.


При работе с XML-файлами:

Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с пространствами имен удобно пользоваться такими функциями:

    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''

    tree = ET.parse(f)
    root = tree.getroot()

    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}

    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...

"""

"""== Получение APPID =="""

"""
Registration - !reCAPTCHA with images!
Get key - !key-TAG without ID|NAME attribute! 
"""

"""== Получение списка городов =="""

import gzip
import json
import os
import requests
import sqlite3 as sql
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_path(filename):
    return os.path.join(SCRIPT_DIR, filename)


class CitiesDB:

    URL = r'http://bulk.openweathermap.org/sample/city.list.json.gz'
    CITY_FILE = r'city.list.json.gz'

    def _check_file_exist(self):
        if not os.path.isfile(get_path(self.CITY_FILE)):
            self._load_from_url()

    def _load_from_url(self):
        response = requests.get(self.URL)
        with open(get_path(self.CITY_FILE), 'wb') as zip:
            zip.write(response.content)

    def find_city_data(self, fields):
        self._check_file_exist()
        with gzip.open(get_path(self.CITY_FILE), 'r') as zip:
            data = json.loads(zip.read().decode('utf-8'))
        return [x for x in data if all([(k, v) in x.items() for k, v in fields.items()])]


"""== Получение погоды =="""


class OpenWeatherAPI:

    ID_FILE = 'app.id'
    REQUEST = r'https://api.openweathermap.org/data/2.5/weather?'

    def __init__(self):
        with open(get_path(self.ID_FILE), 'r') as file:
            self.APPID = file.read()

    def get_data(self, city_id, mode='JSON'):

        request = f'{self.REQUEST}id={city_id}&appid={self.APPID}&units=metric'
        if mode.upper() != 'JSON':
            request += f'&mode={mode.lower()}'

        response = requests.get(request)
        if response.status_code == 200:
            return json.loads(response.content)
        return None


"""== Сохранение данных в локальную БД =="""


class WeatherDB:

    SQL_DB_FILE = 'weather.db'
    SQL_CREATE_DB_FILE = 'create_weather_table.sql'

    def __init__(self):
        self._check_db_file_exist()

    def _execute_command(self, command, need_commit):
        connect = sql.connect(get_path(self.SQL_DB_FILE))
        answer = list(connect.cursor().execute(command))
        if need_commit:
            connect.commit()
        connect.close()
        return answer

    def _check_db_file_exist(self):
        if not os.path.isfile(get_path(self.SQL_DB_FILE)):
            with open(get_path(self.SQL_CREATE_DB_FILE), 'r') as file:
                command = file.read()
            self._execute_command(command, True)

    def _check_data_exist(self, city_id):
        rows = self.get_data({'city_id': city_id})
        return len(rows) != 0

    def get_columns(self):
        connect = sql.connect(get_path(self.SQL_DB_FILE))
        cursor = connect.execute('select * from weather')
        columns = [desc[0] for desc in cursor.description]
        connect.close()
        return columns

    def get_data(self, input_fields=None, output_fields=None):
        """
        Get data from database
        :param input_fields: Dictionary (column|value)
        :param output_fields: List (column)
        :return: List (tuple with columns values)
        """
        if output_fields:
            columns = ",".join(output_fields)
        else:
            columns = '*'
        command = f'SELECT {columns} FROM weather '

        if input_fields:
            conditions = [f'{f} = "{v}"' for f, v in input_fields.items()]
            command += f'WHERE {" AND ".join(conditions)}'
        return self._execute_command(command, False)

    def set_data(self, values):
        """
        Add/update values in database
        :param values: List with values (city_id | city | date | temperature | weather_id | weather_icon)
        """
        if self._check_data_exist(values[0]):
            command = f'UPDATE weather SET temperature="{values[3]}", date="{values[2]}", weather_icon="{values[5]}"' \
                    f' WHERE city_id="{values[0]}"'
        else:
            # values = [f'"{str(x)}"' for x in values]
            values = map(lambda x: f'"{str(x)}"', values)
            command = f'INSERT INTO weather VALUES({",".join(values)})'
        self._execute_command(command, True)


def search_city(country, city):
    print('Search city')
    cities = CitiesDB()
    result = cities.find_city_data({'name': city, 'country': country.upper()})
    if len(result) == 0:
        print('City not found (in list)')
        return None
    if len(result) > 1:
        print('\n'.join([f'{i}. {str(x)}' for i, x in enumerate(result)]))
        index = int(input('Select index correct city:\n'))
        return result[index]
    return result[0]


def get_json_data(city_json):
    print('Download data')
    api = OpenWeatherAPI()
    json_data = api.get_data(city_json['id'])
    if not json_data:
        print('Server not respond')
        return None

    if json_data['cod'] != 200:
        print(json_data['message'])
        return None
    print('Weather data is downloaded')
    return json_data


def update_db(json_data):
    # Add/update data in sql db
    print('Update database')
    weather = WeatherDB()
    weather.set_data([json_data['id'],
                      json_data['name'],
                      datetime.now().strftime('%Y-%m-%d'),
                      json_data['main']['temp'],
                      json_data['weather'][0]['id'],
                      json_data['weather'][0]['icon']])
    print('Database updated')


def main():

    exit_flag = False

    while not exit_flag:
        print('Enter the country and city:')
        country = input('Country - ')
        city = input('City - ')
        city_json = search_city(country, city)
        if city_json:
            json_data = get_json_data(city_json)
            if json_data:
                update_db(json_data)

        answer = input('Add next city?')
        if answer.upper() != 'Y':
            exit_flag = True
        print('-' * 50)


if __name__ == '__main__':
    main()
