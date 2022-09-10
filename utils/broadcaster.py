import asyncio
import logging

from aiogram.utils import exceptions

from loader import bot
from utils.database import MongoDB
from utils.notify_admins import report_log


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender

    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        await report_log(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        await report_log(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        await report_log(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        await report_log(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        await report_log(f"Target [ID:{user_id}]: failed")
    else:
        await report_log(f"Target [ID:{user_id}]: success")
        return True
    return False


async def copy_message(group_id: str, chat_id: int, message_id: int) -> bool:
    """
    Safe messages sender

    :param group_id:
    :param chat_id:
    :param message_id:
    :return:
    """
    try:
        post = await bot.copy_message(group_id, chat_id, message_id)
    except exceptions.BotBlocked:
        await report_log(f"Target [ID:{group_id}]: blocked by user")
    except exceptions.ChatNotFound:
        await report_log(f"Target [ID:{group_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        await report_log(f"Target [ID:{group_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await copy_message(group_id, chat_id, message_id)  # Recursive call
    except exceptions.UserDeactivated:
        await report_log(f"Target [ID:{group_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        await report_log(f"Target [ID:{group_id}]: failed")
    else:
        return post


async def remover(group_id, message_id):
    try:
        await bot.delete_message(group_id, message_id)
    except exceptions.MessageToDeleteNotFound:
        logging.info(f"Message {message_id} not found")
    except exceptions.MessageCantBeDeleted:
        logging.info(f"Message {message_id} can't be deleted")
    except exceptions.RetryAfter as e:
        await report_log(f"Target [ID:{group_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await remove_posts(group_id, message_id)  # Recursive call
    except exceptions.TelegramAPIError:
        logging.info(f"Target [ID:{group_id}]: failed")
    else:
        return True
    return False


async def remove_posts(group_id: str, last_post):
    """
    Remove old posts

    :param group_id: str
    :param last_post: bson object
    :return:
    """
    async for post in MongoDB.get_data_base().posts.find({"group_id": str(group_id)}):
        if post.get('_id') == last_post:
            continue

        await remover(group_id, post.get('message_id'))
        await MongoDB.get_data_base().posts.delete_one({"_id": post.get('_id')})
