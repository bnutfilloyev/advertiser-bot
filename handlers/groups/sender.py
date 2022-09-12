import logging

from aiogram.types import Message, ContentType

from filters import IsGroup
from loader import dp
from utils.broadcaster import forward_message, remove_posts, copy_message
from utils.database import MongoDB
from utils.notify_admins import report_log


@dp.message_handler(IsGroup(), content_types=ContentType.ANY)
async def echo(message: Message):
    group_id = message.chat.id
    post = await MongoDB.get_post(str(group_id))

    if post is None:
        await report_log("No post found")

    chat_id = post.get('chat_id')
    message_id = post.get('message_id')

    if post.get('post_type') == 'forward':
        new_post = await forward_message(group_id, chat_id, message_id)
    else:
        new_post = await copy_message(group_id, chat_id, message_id)

    if new_post is None:
        logging.info("Request not found {}".format(message_id))
        return

    res = await MongoDB.set_post(str(group_id), new_post.message_id, chat_id)

    if res is None:
        logging.info("Response not found {}".format(new_post.message_id))
        return

    await MongoDB.update_groups(str(group_id), {"last_post": res})
    await remove_posts(group_id, res)
