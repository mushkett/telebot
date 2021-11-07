from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import CallbackQuery

from aiogram.utils import executor
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
    try:
        answer3 = message.text
        await state.update_data(city=answer3)
        data = await state.get_data()
        set_location(message.chat.id, data.get("country"), data.get("state"), data.get("city"))
        await message.answer('Thank you! Now you can get weather forecast', reply_markup=mainMenu)
    except TypeError as ex:
        await message.answer(f'{ex}, try again please')
    finally:
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
async def get_3_days_weather(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(text=f'{weather.weather_several_days(call.from_user.id, 5)}')
    await call.message.answer(text='Forecast for', reply_markup=mainMenu)



@dp.message_handler()
async def command_nof_found(message: types.Message):
    await message.reply('Command not found!')


executor.start_polling(dp, skip_updates=True)
