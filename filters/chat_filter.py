from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsChannel(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.CHANNEL


class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type in [types.ChatType.SUPERGROUP, types.ChatType.GROUP]


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE
