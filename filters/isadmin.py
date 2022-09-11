from aiogram.dispatcher.filters import BoundFilter

from loader import config


class IsAdmin(BoundFilter):
    async def check(self, message):
        return str(message.from_user.id) in config.bot.admins
