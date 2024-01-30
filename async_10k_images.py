import time
import aiofiles
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from itertools import chain


def get_folder_size(filepath, size=0):
    for root, dirs, files in os.walk(filepath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size


async def write_file(session, url, name):
    async with aiofiles.open(f'images/{name}', mode='wb') as file:
        async with session.get(url) as response:
            async for x in response.content.iter_chunked(5120):
                await file.write(x)
    

async def get_pages_urls(session, web_url):
    async with session.get(web_url) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        pages = (urljoin(web_url, i['href']) for i in soup.find_all(class_='lnk_img'))
        return pages


async def get_pages_urls_level2(session, web_url):
    async with session.get(web_url) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        pages = (urljoin(web_url, i['href']) for i in soup.find_all(class_='lnk_img'))
        return pages


async def get_images_urls(session, url, semaphore):
    async with semaphore:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            img_urls = (urljoin(url, img['src']) for img in soup.find_all(class_='picture'))
            return img_urls


async def main():
    web_url = 'https://parsinger.ru/asyncio/aiofile/3/index.html'
    semaphore = asyncio.Semaphore(50)
    async with aiohttp.ClientSession() as session:
        pages_urls = await get_pages_urls(session, web_url)
        task = (get_pages_urls_level2(session, x) for x in pages_urls)
        inner_pages = await asyncio.gather(*task) #[[urls...],[urls...]]
        inner_task = (get_images_urls(session, page, semaphore) for page in chain.from_iterable(inner_pages))
        lists_images = await asyncio.gather(*inner_task)
        images_urls = (write_file(session, url, url.rsplit('/',1)[1]) for url in set(chain.from_iterable(lists_images)))
        await asyncio.gather(*images_urls)


start = time.perf_counter()
asyncio.run(main())
print(get_folder_size('images'))
end = time.perf_counter()
print(end - start)
