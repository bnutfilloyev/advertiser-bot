from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.database import MongoDB

group_cb = CallbackData('group', 'group_id')
setting_cb = CallbackData('setting', 'setting_name')


async def groups_list():
    btn = InlineKeyboardMarkup()
    async for group in MongoDB.get_groups():
        btn.add(InlineKeyboardButton(text=group['group_name'], callback_data=group_cb.new(group_id=group['group_id'])))
    return btn


async def post_settings():
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💾 Postni ko'rish",
                                     callback_data=setting_cb.new(setting_name='get_post')),
                InlineKeyboardButton(text="🔧 Postni o'zgartirish",
                                     callback_data=setting_cb.new(setting_name='set_post')),
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data=setting_cb.new(setting_name='back'))
            ]
        ]
    )
