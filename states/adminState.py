from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    adminState = State()
    SendUsers = State()
    SendGroups = State()

