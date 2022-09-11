from loader import dp, bot

from utils.database import MongoDB
from aiogram.types import Message


@dp.message_handler(content_types=['any'])
async def test(message: Message):
    print(message)
    post = await bot.forward_message(chat_id="-1001530205550", from_chat_id=message.chat.id, message_id=message.message_id)
    print(post)
