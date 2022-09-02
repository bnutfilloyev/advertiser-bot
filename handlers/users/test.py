from aiogram.types import Message, ContentType

from loader import dp, bot


@dp.message_handler(content_types=ContentType.ANY)
async def echo(message: Message):
    await bot.copy_message("-1001530205550", message.chat.id, "2868")
    await message.forward(message.chat.id)
    await message.copy_to("-1001530205550", "2868")
