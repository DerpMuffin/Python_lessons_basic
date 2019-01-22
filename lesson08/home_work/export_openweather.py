
""" OpenWeatherMap (экспорт)

Сделать скрипт, экспортирующий данные из базы данных погоды, 
созданной скриптом openweather.py. Экспорт происходит в формате CSV или JSON.

Скрипт запускается из командной строки и получает на входе:
    export_openweather.py --csv filename [<город>]
    export_openweather.py --json filename [<город>]
    export_openweather.py --html filename [<город>]
    
При выгрузке в html можно по коду погоды (weather.id) подтянуть 
соответствующие картинки отсюда:  http://openweathermap.org/weather-conditions

Экспорт происходит в файл filename.

Опционально можно задать в командной строке город. В этом случае 
экспортируются только данные по указанному городу. Если города нет в базе -
выводится соответствующее сообщение.

"""

import sys
import csv
import json
from openweather import WeatherDB


generates = {
    'csv': lambda f, c, d: gen_csv(f, c, d),
    'json': lambda f, c, d: gen_json(f, c, d),
    'html': lambda f, c, d: gen_html(f, c, d)
}
html_template = 'html_template.html'
html_main = ''
div_content = r"""
<div>
    <b>CITY</b> <br>
    <img src="IMG" alt="icon" width="50">
    <b>TEMP &deg;C</b> <br>
    <span>DATE</span>
</div>
"""
IMG_URL = 'http://openweathermap.org/img/w/'


def load_html_template():
    global html_main
    with open(html_template, 'r') as file:
        html_main = file.read()


def _check_file_ext(filename, ext):
    if filename.endswith(f'.{ext}'):
        return filename
    return f'{filename}.{ext}'


def _get_dicts(keys, values):
    dict_lambda = lambda v: dict(map(lambda i, k: (k, v[i]), range(len(keys)), keys))
    return [dict_lambda(v) for v in values]


def gen_csv(file, cols, data):
    writer = csv.DictWriter(file, cols)
    writer.writeheader()
    rows = _get_dicts(cols, data)
    writer.writerows(rows)


def gen_json(file, cols, data):
    json_data = _get_dicts(cols, data)
    json.dump(json_data, file)
    pass


def gen_html(file, cols, data):
    load_html_template()
    html = html_main
    content = ''
    for d in data:
        img = f'{IMG_URL}{d[5]}.png'
        div = div_content.replace('CITY', d[1]).replace('DATE', str(d[2]))\
            .replace('TEMP', str(int(d[3]))).replace('IMG', img)
        content += div

    html = html.replace('CONTENT', content)
    file.write(html)


def main():

    if len(sys.argv) < 3:
        print('Incorrect amount of args')
        return

    convert_type = sys.argv[1][2:]
    if convert_type not in generates.keys():
        print(f'Incorrect convert type - {convert_type}')
        return

    arg = {}
    if len(sys.argv) == 4:
        arg['city'] = sys.argv[3]

    print('Read Database')
    weather = WeatherDB()
    cols = weather.get_columns()
    data = weather.get_data(arg)

    if len(data) == 0:
        print('Data of the city not found')
        return

    filename = _check_file_ext(sys.argv[2], convert_type)

    print(f'Exporting to {filename}')
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        generates[convert_type](file, cols, data)
    print('Complete')


if __name__ == '__main__':
    main()

