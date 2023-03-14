from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(row_width=1).add(
                               InlineKeyboardButton(text='Активировать', callback_data='enable'),
                               InlineKeyboardButton(text='Остановить', callback_data='disable'),
                               InlineKeyboardButton(text='Статистика', callback_data='stat'),
                               InlineKeyboardButton(text='Настройки', callback_data='config'))


cancel = InlineKeyboardMarkup(row_width=1).add(
                                   InlineKeyboardButton(text='Назад', callback_data='cancel'))


admin_kb = InlineKeyboardMarkup(row_width=2).add(
                                   InlineKeyboardButton(text='Вкл', callback_data='admin_on'),
                                   InlineKeyboardButton(text='Выкл', callback_data='admin_off'),
                                   InlineKeyboardButton(text='Назад', callback_data='cancel'))

