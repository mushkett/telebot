from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext

from aiogram.utils import executor
import weather
from FSM import location_states
from configparser import ConfigParser
from database import set_location


config = ConfigParser()
config.read('config.ini')
TOKEN = config.get('auth', 'TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    await message.reply("Hello, I'm weather bot. \n \n"
                        "I can send you weather forecast:\n"
                        "For 1 day (/get_1_day_weather)\n"
                        "For 3 days (/get_3_days_weather)\n"
                        "For 5 days (/get_5_days_weather)"
                        "\n\n"
                        "But only after you enter you current location (/set_location)")


@dp.message_handler(commands=['set_location'], state=None)
async def enter_location_config(message: types.Message):
    await message.answer("Input your country")

    await location_states.country.set()


@dp.message_handler(state=location_states.country)
async def answer_country(message: types.Message, state: FSMContext):
    answer1 = message.text
    await state.update_data(country=answer1)

    await message.answer('Input your state\n'
                         'Example: "Sumy Oblast"')
    await location_states.next()


@dp.message_handler(state=location_states.state)
async def answer_state(message: types.Message, state: FSMContext):
    answer2 = message.text
    await state.update_data(state=answer2)
    await message.answer('Input your city')
    await location_states.next()


@dp.message_handler(state=location_states.city)
async def answer_state(message: types.Message, state: FSMContext):
    await message.answer('Thank you! Now you can get weather forecast')
    answer3 = message.text
    await state.update_data(city=answer3)
    data = await state.get_data()
    set_location(message.chat.id, data.get("country"), data.get("state"), data.get("city"))
    await state.finish()


@dp.message_handler(commands=['get_1_day_weather'])
async def get_weather(message: types.Message):
    await message.answer(weather.weather_1_day(message.chat.id))


@dp.message_handler(commands=['get_3_days_weather'])
async def get_3_days_weather(message: types.Message):
    await message.answer(weather.weather_several_days(message.chat.id, 3))


@dp.message_handler(commands=['get_5_days_weather'])
async def get_3_days_weather(message: types.Message):
    await message.answer(weather.weather_several_days(message.chat.id, 5))


@dp.message_handler()
async def command_nof_found(message: types.Message):
    await message.reply('Command not found!')


executor.start_polling(dp, skip_updates=True)
