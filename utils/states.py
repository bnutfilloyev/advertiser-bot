from aiogram.dispatcher.filters.state import StatesGroup, State


class AddGroup(StatesGroup):
    GetGroupName = State()
    GetGroupId = State()


class Advertisement(StatesGroup):
    GetAdvertisement = State()


class RemoveGroup(StatesGroup):
    GetGroupId = State()
