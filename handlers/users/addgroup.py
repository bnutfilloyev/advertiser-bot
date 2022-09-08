from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import IsPrivate
from loader import dp
from utils.database import MongoDB
from utils.states import AddGroup


@dp.message_handler(IsPrivate(), Command("addgroup"), state="*")
async def add_group(msg: types.Message):
    await msg.answer("<b>⌨️Guruh nominini kiriting:</b>")
    await AddGroup.GetGroupName.set()


@dp.message_handler(state=AddGroup.GetGroupName)
async def get_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group_name'] = msg.text
    await msg.answer("<b>🆔Guruh ID'sini kiriting:</b>")
    await AddGroup.GetGroupId.set()


@dp.message_handler(state=AddGroup.GetGroupId)
async def get_id(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await MongoDB.add_group(group_name=data['group_name'], group_id=msg.text)
    await msg.answer("<b>✅ Guruh qo'shildi.</b>")
    await state.finish()
