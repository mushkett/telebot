from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

mainMenu = InlineKeyboardMarkup(row_width=3)

weather1Btn = InlineKeyboardButton("1 day", callback_data='get_1_day_weather')
weather3Btn = InlineKeyboardButton("3 days", callback_data='get_3_days_weather')
weather5Btn = InlineKeyboardButton("5 days", callback_data='get_5_days_weather')
mainMenu.insert(weather1Btn)
mainMenu.insert(weather3Btn)
mainMenu.insert(weather5Btn)


