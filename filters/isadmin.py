from aiogram.dispatcher.filters import BoundFilter

from loader import config


class IsAdmin(BoundFilter):
    async def check(self, message):
        return message.from_user.id in config.bot.admins
