from aiogram.types import Message, ContentType
from aiogram.utils import exceptions

from loader import dp, bot
from utils.database import MongoDB


@dp.message_handler(content_types=ContentType.ANY)
async def echo(message: Message):
    group_id = message.chat.id
    post = await MongoDB.get_post(str(group_id))

    if post is None:
        return

    chat_id = post.get('chat_id')
    message_id = post.get('message_id')
    new_post = await bot.copy_message(group_id, chat_id, message_id)

    if post.get('last_message_id') is None:
        await MongoDB.update_post(str(group_id), {'last_message_id': new_post.message_id})
        return

    try:
        await bot.delete_message(group_id, post.get('last_message_id'))
    except exceptions.MessageToDeleteNotFound:
        pass

    await MongoDB.update_post(str(group_id), {'last_message_id': new_post.message_id})
