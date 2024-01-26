import requests
from bs4 import BeautifulSoup
import lxml
import csv


def resoup_func(url, session):
        """
        Make an HTTP request to the given URL, handle potential exceptions, and return a BeautifulSoup object.

        Parameters:
        - url: to make the request to.

        Returns:
        - BeautifulSoup or None: Successful parsing or None in case of an error.
        """
        try:
            res = session.get(url=url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'lxml')
            return soup
        except requests.RequestException as e:
            print(f'Error: {e}\n')

def main():


    with open('file.csv', 'w', encoding='utf-8', newline='') as file:

        header = 'Наименование;Артикул;Бренд;Модель;Наличие;Цена;Старая цена;Ссылка;'.split(';')
        writer = csv.writer(file, delimiter=';')
        writer.writerow(header)

        with requests.Session() as rs:
            
            original_url = 'https://parsinger.ru/html/index1_page_1.html'
            base = original_url.rsplit('/', 1)[0]
            resoup = resoup_func(original_url, rs)

            if resoup:
                for index in resoup.find(class_='nav_menu').find_all('a'):
                    index_resoup = resoup_func(f'{base}/{index["href"]}', rs)

                    if index_resoup is None:
                        continue

                    for page in index_resoup.find(class_='pagen').find_all('a'):
                        page_resoup = resoup_func(f'{base}/{page["href"]}', rs)

                        if page_resoup is None:
                            continue

                        for item in page_resoup.find_all(class_='name_item'):

                            item_url = f'{base}/{item["href"]}'
                            item_resoup = resoup_func(item_url, rs)
                            
                            try:
                                # Extract data
                                name = item_resoup.find(id='p_header').text.strip()
                                # Article, brand, model and in_stock
                                art_brand_mod_stock = (
                                    i.text.split(': ')[1].strip() 
                                    for i in item_resoup.select('.article, #brand, #model, #in_stock')
                                    )
                                prices = (p.text.strip() for p in  item_resoup.select('#price, #old_price'))

                                # Write to CSV
                                writer.writerow((name, *art_brand_mod_stock, *prices, item_url))

                            except Exception as e:
                                print(f'Error processing item: {item_url}')
                                print(f'Error: {e}')
                                continue
            else:
                print(f'Something went wrong with the url: {original_url}\n\nFix it and try again')


if __name__ == '__main__':
    main()