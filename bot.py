from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
import functions
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
    await message.reply('Привет! Я погодный бот')


@dp.message_handler(commands=['set_location'], state=None)
async def enter_location_config(message: types.Message):
    await message.answer("Input your country")

    await location_states.country.set()


@dp.message_handler(state=location_states.country)
async def answer_country(message: types.Message, state: FSMContext):
    answer1 = message.text
    await state.update_data(country=answer1)

    await message.answer('Input your state')
    await location_states.next()


@dp.message_handler(state=location_states.state)
async def answer_state(message: types.Message, state: FSMContext):
    answer2 = message.text
    await state.update_data(state=answer2)
    await message.answer('Input your city')
    await location_states.next()


@dp.message_handler(state=location_states.city)
async def answer_state(message: types.Message, state: FSMContext):
    answer3 = message.text
    await state.update_data(city=answer3)
    data = await state.get_data()
    set_location(message.chat.id, data.get("country"), data.get("state"), data.get("city"))


@dp.message_handler(commands=['Get_weather'])
async def get_weather(message: types.Message):
    await message.answer(functions.print_weather(city_name='Сумы'))


@dp.message_handler()
async def command_nof_found(message: types.Message):
    await message.reply('Команда не найдена')


executor.start_polling(dp, skip_updates=True)
