import requests
from bs4 import BeautifulSoup
import json

def resoup_func(url):
        """
        Make an HTTP request to the given URL, handle potential exceptions, and return a BeautifulSoup object.

        Parameters:
        - url: to make the request to.

        Returns:
        - BeautifulSoup or None: Successful parsing or None in case of an error.
        """
        try:
            res = rs.get(url=url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'lxml')
            return soup
        except requests.RequestException as e:
            print(f'Error: {e}\n')



with requests.Session() as rs:

    original_url = 'https://parsinger.ru/html/index1_page_1.html'
    base = original_url.rsplit('/', 1)[0]
    resoup = resoup_func(original_url)
    all = []
    if resoup:
        for index in resoup.find(class_='nav_menu').find_all('a'):
            index_resoup = resoup_func(f'{base}/{index["href"]}')

            for page in index_resoup.find(class_='pagen').find_all('a'):
                page_resoup = resoup_func(f'{base}/{page["href"]}')

                for i in page_resoup.find_all(class_='item'):
                    all.append({
                    'Наименование': i.find(class_='name_item').text.strip(),
                    **{
                        key.strip(): value.strip() 
                        for desc in i.find_all('li')
                        for key, value in [desc.text.strip().split(': ')]
                        },
                    'Цена': i.find(class_='price').text.strip()
                    }
                    )

with open('file.json', 'w', encoding='utf-8') as file:
    json.dump(all, file, indent=4, ensure_ascii=False)