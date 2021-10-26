from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import functions

import os

CITY_NAME = 'Сумы'

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


'''@dp.message_handler()
async def echo_send(message: types.Message):
   # await message.answer(message.text)
    await message.reply(message.text)
   # await bot.send_message(message.from_user.id, message.text)'''


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    await message.reply('Привет! Я погодный бот')


@dp.message_handler(commands=['Get_weather'])
async def get_weather(message: types.Message):
    await message.answer(functions.print_weather(city_name='Сумы'))


@dp.message_handler()
async def command_nof_found(message: types.Message):
    await message.reply('Команда не найдена')

executor.start_polling(dp, skip_updates=True)
