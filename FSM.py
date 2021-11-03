from aiogram.dispatcher.filters.state import StatesGroup, State

class location_states(StatesGroup):
    country = State()
    state = State()
    city = State()
