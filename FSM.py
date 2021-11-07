from aiogram.dispatcher.filters.state import StatesGroup, State

class location_states(StatesGroup):
    input_city = State()
    choose_city = State()

