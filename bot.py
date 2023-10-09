from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import CallbackQuery

from aiogram.utils import executor

import geocoding_API
import weather
from FSM import location_states
from configparser import ConfigParser
from database import set_location
from keyboard import mainMenu

config = ConfigParser()
config.read('config.ini')
TOKEN = config.get('auth', 'TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    await message.reply("Hello, I'm weather bot. \n \n"
                        "At first you should set your location \n\n"
                        "/set_location")


@dp.message_handler(commands=['set_location'], state=None)
async def enter_location_config(message: types.Message):
    await message.answer("Input your city")

    await location_states.input_city.set()


@dp.message_handler(state=location_states.input_city)
async def input_city(message: types.Message, state: FSMContext):
    city_name = message.text  # city name
    locations_dict = geocoding_API.get_city_list(city_name)
    location_list_answer = 'Choose your county (number only):\n'
    for i in locations_dict:
        location_list_answer += f'{i}.{locations_dict[i]}\n'
    await message.answer(location_list_answer)
    await state.update_data(city=city_name)
    await state.update_data(dict=locations_dict)
    await location_states.choose_city.set()


@dp.message_handler(state=location_states.choose_city)
async def choose_city(message: types.Message, state: FSMContext):
    location_number = message.text
    data = await state.get_data()
    dict1 = data.get('dict')
    if set_location(chat_id=message.chat.id, country=dict1[int(location_number)], city=data.get('city')) != 0:
        set_location(chat_id=message.chat.id, country=dict1[int(location_number)], city=data.get('city'))
        await message.answer('Thank you! Now you can get weather forecast', reply_markup=mainMenu)

    await state.finish()


@dp.message_handler(commands=['menu'])
async def send_menu(message: types.Message):
    await message.answer(text='Forecast for ', reply_markup=mainMenu)


@dp.callback_query_handler(text='get_1_day_weather')
async def get_weather(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(text=f'{weather.weather_1_day(call.from_user.id)}')
    await call.message.answer(text='Forecast for ', reply_markup=mainMenu)


@dp.callback_query_handler(text='get_3_days_weather')
async def get_3_days_weather(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(text=f'{weather.weather_several_days(call.from_user.id, 3)}')
    await call.message.answer(text='Forecast for', reply_markup=mainMenu)


@dp.callback_query_handler(text='get_5_days_weather')
async def get_5_days_weather(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(text=f'{weather.weather_several_days(call.from_user.id, 5)}')
    await call.message.answer(text='Forecast for', reply_markup=mainMenu)


@dp.message_handler()
async def command_nof_found(message: types.Message):
    await message.reply('Command not found!')


executor.start_polling(dp, skip_updates=True)
