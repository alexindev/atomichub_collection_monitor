import asyncio
import tls_client
from loguru import logger
from aiogram.utils.exceptions import BotBlocked

from config import headers, get_json


async def start_parsing(bot, user, base):
    session = tls_client.Session(client_identifier="chrome_110")
    base.create_table()

    old_collection = base.get_all_project()
    new_collection = []
    count = 1
    do = True
    while do:
        names = []
        response = session.post('https://wax.api.aa.atomichub.io/atomicmarket/v1/stats/collections',
                                headers=headers,
                                json=get_json(count)
                                ).json()
        for data in response['data']['results']:
            collection_name = data['collection_name']
            name = data['name']
            author = data['author']
            fee = data['market_fee'] * 100
            url = f'https://wax.atomichub.io/explorer/collection/wax-mainnet/{collection_name}'

            if not base.get_project(collection_name):
                base.add_data(collection_name, name, author, fee, url)
                await asyncio.sleep(1)
                text = f'🔥<b>️Новая коллекция!</b>🔥' \
                       f'\n<b>Коллекция:</b> {collection_name}' \
                       f'\n<b>Название:</b> {name}' \
                       f'\n<b>Создатель:</b> {author}' \
                       f'\n<b>Комиссия: </b> {fee}' \
                       f'\n<b>Ссылка: </b> {url}'

                try:
                    bot.send_message(user,
                                     text=text,
                                     disable_web_page_preview=True,
                                     parse_mode='HTML'
                                     )
                except BotBlocked:
                    logger.error('bot block')
                    base.del_user(user)
                except:
                    pass

            names.append(collection_name)
            new_collection.append((collection_name,))

        count += 1

        if len(names) != 50:
            do = False
        else:
            names.clear()

    deleted_data = set(old_collection) - set(new_collection)
    if deleted_data:
        try:
            for data in deleted_data:
                projects = base.get_project(data[0])
                if projects:
                    collection_name = projects[0]
                    name = projects[1]
                    author = projects[2]

                    text = f'<b>❗️ Коллекция удалена ❗️</b>' \
                           f'\n<b>Коллекция:</b> {collection_name}' \
                           f'\n<b>Название:</b> {name}' \
                           f'\n<b>Создатель:</b> {author}'
                    await asyncio.sleep(1)
                    try:
                        bot.send_message(user,
                                         text=text,
                                         parse_mode='HTML',
                                         disable_web_page_preview=True
                                         )
                    except BotBlocked:
                        logger.error('bot block')
                        base.del_user(user)
                    except:
                        pass
                    base.delete_project(data[0])

        except Exception as e:
            logger.error(e)
