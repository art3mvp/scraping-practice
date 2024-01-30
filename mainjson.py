import requests
from bs4 import BeautifulSoup
import lxml
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
    extracted_data = []

    if resoup:
        for index in resoup.find(class_='nav_menu').find_all('a'):
            index_resoup = resoup_func(f'{base}/{index["href"]}')

            if index_resoup is None:
                continue

            for page in index_resoup.find(class_='pagen').find_all('a'):
                page_resoup = resoup_func(f'{base}/{page["href"]}')

                if page_resoup is None:
                    continue
        
                for item in page_resoup.find_all(class_='name_item'):
                    item_url = f'{base}/{item["href"]}'
                    item_resoup = resoup_func(item_url)
                    
                    extracted_data.append(
                            {
                    'categories': item['href'].split('/')[0],
                    'name': item_resoup.find(id='p_header').text.strip(),
                    'article': item_resoup.find(class_='article').text.split(': ')[1].strip(),
                    'description': {
                        desc['id'].strip(): desc.text.split(': ')[1].strip()
                        for desc in item_resoup.find_all('li')
                        },
                    'count': item_resoup.find(id='in_stock').text.split(': ')[1].strip(),
                    **{sp['id']: sp.text.strip() for sp in item_resoup.select('#price, #old_price')},
                    'link': item_url
                    }
                    )
    else:
        print(f'Something went wrong with the url: {original_url}\n\nFix it and try again')

with open('file.json', 'w', encoding='utf-8') as file:
    json.dump(extracted_data, file, indent=4, ensure_ascii=False)
    