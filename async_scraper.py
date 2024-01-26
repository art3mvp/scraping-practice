import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time 
import csv
from itertools import chain


async def get_categories(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        categories = [urljoin(url, cat['href']) for cat in soup.find(class_='nav_menu').find_all('a')]
        return categories


async def get_pages(session, category_url):
    async with session.get(category_url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        pages = [urljoin(category_url, pag['href']) for pag in soup.find(class_='pagen').find_all('a')]
        return pages
    

async def get_products(session, page_url):
    async with session.get(page_url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        products = [urljoin(page_url, product['href']) for product in soup.find_all(class_='name_item')]
        return products


async def get_product_data(session, product_url):
    async with session.get(product_url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        name = soup.find(id='p_header').text
        article_desc_stock = (
            i.text.split(': ')[1].strip()
            for i in soup.select('.article, li, #in_stock')
        )
        prices  = (
            i.text.strip() for i in soup.select('#price, #old_price')
        )
        item_data = chain([name, product_url], article_desc_stock, prices)
        return item_data


async def get_products_info(session):
    categories = await get_categories(session, 'https://parsinger.ru/html/index1_page_1.html')
    tasks = []
    for category in categories:
        pages = await get_pages(session, category)
        tasks.extend(get_products(session, page) for page in pages)
    products_urls = await asyncio.gather(*tasks)
    tasks_data_extract = [get_product_data(session, url) for url in chain.from_iterable(products_urls)]    
    products_info = await asyncio.gather(*tasks_data_extract)
    return products_info


async def main():
    async with aiohttp.ClientSession() as session:
        products_data = await get_products_info(session)
        with open ('file.csv', 'w', encoding='utf-8', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerows(products_data)


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(end - start)
