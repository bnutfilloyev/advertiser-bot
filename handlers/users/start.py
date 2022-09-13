from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from filters import IsAdmin
from keyboards.inline import groups_list
from loader import dp


@dp.message_handler(IsAdmin(), CommandStart(), state='*')
async def cmd_start(msg: Message, state: FSMContext):
    await msg.answer("<b>📝 Guruhlar ro'yxati: </b>", reply_markup=await groups_list())
    await state.finish()
