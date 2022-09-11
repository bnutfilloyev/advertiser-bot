from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from filters import IsAdmin
from keyboards.inline import groups_list, group_cb
from loader import dp
from utils.database import MongoDB
from utils.states import RemoveGroup


@dp.message_handler(IsAdmin(), commands=['removegroup'], state="*")
async def remove_group(message: Message):
    await message.answer("O'chirmoqchi bo'lgan guruhni tanlang.", reply_markup=await groups_list())
    await RemoveGroup.GetGroupId.set()


@dp.callback_query_handler(group_cb.filter(), state=RemoveGroup.GetGroupId)
async def remove_group(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await MongoDB.remove_group(group_id=callback_data['group_id'])
    await call.message.answer(f"Guruh o'chirildi.")
    await state.finish()
