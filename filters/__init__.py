from aiogram import Dispatcher

from loader import dp
from .chat_filter import IsChannel, IsGroup, IsPrivate

if __name__ == "filters":
    dp.filters_factory.bind(IsChannel)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)

