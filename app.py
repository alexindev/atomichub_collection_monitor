import asyncio
from loguru import logger
from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher.filters import Text

from config import *
from database import Database
from bot import start_parsing
from kb import *

bot = Bot(TOKEN)
dp = Dispatcher(bot)
base = Database()


# проверка подписки
async def check_subsciber(chat_member):
    return True if chat_member['status'] != 'left' else False


@dp.message_handler(commands=['start'])
async def chatid(message: types.Message):
    try:
        if await check_subsciber(await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)):
            base.create_user_table()
            if not base.get_user(message.from_user.id):
                base.add_user(message.from_user.id, 3)
            await bot.send_message(message.from_user.id,
                                   text='Выбери команду:',
                                   reply_markup=main_menu)
        else:
            await bot.send_message(message.from_user.id, 'Только для подписчиков канала "кодим ~ криптуем"')
    except Exception as e:
        logger.error(e)


# настройки админа
@dp.callback_query_handler(lambda call: call.data == 'config')
async def on_mess(callback: types.CallbackQuery):
    await callback.answer()
    if callback.from_user.id in admins:
        await bot.send_message(callback.from_user.id, 'Настройки',
                               reply_markup=admin_kb)
    else:
        await bot.send_message(callback.from_user.id, 'Нет доступа',
                               reply_markup=cancel)


# управление рассылкой
@dp.callback_query_handler(Text(startswith='admin_'))
async def on_mess(callback: types.CallbackQuery):
    comand = callback.data.split('_')[1]
    if comand == 'on':
        await callback.answer('Рассылка включена')
        do = True
    else:
        await callback.answer('Рассылка выключена')
        do = False
    while do:
        users = base.get_users(1)
        for user in users:
            await start_parsing(bot, user[0], base)
        await asyncio.sleep(3600)


# добавить в рассылку
@dp.callback_query_handler(lambda call: call.data == 'enable')
async def on_mess(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text='Рассылка активирована')
    base.change_status(callback.from_user.id, 1)


# отключить рассылку
@dp.callback_query_handler(lambda call: call.data == 'disable')
async def off_mess(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text='Рассылка отключена')
    base.change_status(callback.from_user.id, 0)


# статистика
@dp.callback_query_handler(lambda call: call.data == 'stat')
async def stat(callback: types.CallbackQuery):
    await callback.answer()
    count = base.collection_count()
    await bot.send_message(callback.from_user.id, text=f'В данный момемент в базе {count[0]} коллекций',
                           reply_markup=cancel)


# на главную
@dp.callback_query_handler(lambda call: call.data == 'cancel')
async def cancel(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id,
                           text='Выбери команду:',
                           reply_markup=main_menu)


async def set_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота")
    ])


async def on_stratup(dp):
    logger.info('Bot started')
    await set_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_stratup)
