from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from filters import IsPrivate
from keyboards.inline import groups_list
from loader import dp


@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def cmd_start(msg: Message):
    await msg.answer("<b>📝 Guruhlar ro'yxati: </b>", reply_markup=await groups_list())
