import requests
from bs4 import BeautifulSoup
from itertools import cycle
import lxml
import json


def get_columns(tag):
    return f'{tag}:nth-child(1), {tag}:nth-child(2), {tag}:nth-child(5), {tag}:nth-child(8)'


def valid(d):
    if d.get('Стоимость авто') <= 4000000 and d.get('Год выпуска') >= 2005 and d.get('Тип двигателя') == "Бензиновый":
        return d


def int_type(data):
    return data if not data.isdigit() else int(data)

def main():
    response = requests.get(url='https://parsinger.ru/4.8/6/index.html')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    header, *rows = soup.find_all('tr')
    all_cars = []

    for i in rows:
        if car:= valid({k.text: int_type(v.text) for k, v in zip(header.select(get_columns('th')), i.select(get_columns('td')))}):
            all_cars.append(car)
        
        
    print(json.dumps(sorted(all_cars, key=lambda x: x['Стоимость авто']), indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()