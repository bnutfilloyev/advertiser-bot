from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from loader import dp
from utils.database import MongoDB

db = MongoDB.get_data_base()


@dp.message_handler(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer("<b>🂠Guruhlar ro'yxati: </b>")
