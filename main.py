import requests
from bs4 import BeautifulSoup
from itertools import cycle
import lxml
import json


def get_columns(r, tag):
    columns = f'{tag}:nth-child(1), {tag}:nth-child(2), {tag}:nth-child(5), {tag}:nth-child(8)'
    return [int_type(i.text) for i in r.select(columns)]


def int_type(data):
    return data if not data.isdigit() else int(data)


def valid(data_list):
    if data_list[-1] <= 4000000 and data_list[1] >= 2005 and data_list[2] == "Бензиновый":
        return data_list


def main():
    response = requests.get(url='https://parsinger.ru/4.8/6/index.html')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    header, *rows = soup.find_all('tr')
    header = get_columns(header, 'th')
    all_cars = []

    for i in rows:
        if car:= valid(get_columns(i, 'td')):
            all_cars.append(dict(zip(header, car)))
        
        
    print(json.dumps(sorted(all_cars, key=lambda x: x['Стоимость авто']), indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()