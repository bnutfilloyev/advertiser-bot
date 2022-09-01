from aiogram.types import Message

from loader import dp

advertisement = "This is advertisement"
last_message_id = 123456789


@dp.message_handler()
async def sender(message: Message):
    ...
