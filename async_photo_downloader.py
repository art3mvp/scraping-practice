from pyrogram import Client
from pyrogram.enums import MessagesFilter
import os
import asyncio
from dotenv import load_dotenv

def calculate_directory_size(path):
    total_size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size
    
    
async def downloader(app, message):
    await app.download_media(message.photo, file_name=f"images/{message.id}.png")


async def main():
    async with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
        tasks = [downloader(app, message) async for message in 
                 app.get_chat_history(chat_id=group_url, filter=MessagesFilter.PHOTO)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    load_dotenv()

    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    group_url = 'parsinger_pyrogram'
    asyncio.run(main())
    print(calculate_directory_size('photos'))