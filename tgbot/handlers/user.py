from aiogram import Dispatcher
from aiogram.types import Message

#from tgbot.services.repository import Repo


async def user_start(m: Message):
#    await repo.add_user(m.from_user.id)
    await m.reply("""
            Привет, дорогой друг✊ \
            \nЯ - твой личный помощник в мире спорта! \
            \nВ управлении я прост, достаточно нажать на меню, которое ты уже использовал, скорее всего. \
            \nВ нем выбери нужный пункт и погнали!🚀""")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
