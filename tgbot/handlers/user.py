from aiogram import Dispatcher
from aiogram.types import Message

#from tgbot.services.repository import Repo
from database.database_actions import connection, add_user


async def user_start(message: Message):
    user_in_database = add_user(connection, user_id=message.from_user.id, user_name=message.from_user.first_name)
    if user_in_database:
        await message.reply(
            f"""
            {message.from_user.first_name}, привет. Мы уже знакомились с тобой. \
            \nТы все так же можешь управлять пунктами меню 😉
            """
                )
    else:
        await message.reply("""
                Привет, дорогой друг✊ \
                \nЯ - твой личный помощник в мире спорта! \
                \nВ управлении я прост, достаточно нажать на меню, которое ты уже использовал, скорее всего. \
                \nВ нем выбери нужный пункт и погнали!🚀""")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
