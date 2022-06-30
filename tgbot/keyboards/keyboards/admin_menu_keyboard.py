from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



admin_actions = ReplyKeyboardMarkup([
    [KeyboardButton("Add exercise")],
    [KeyboardButton("Delete exercise"), KeyboardButton("Change exercise")]

    ])
