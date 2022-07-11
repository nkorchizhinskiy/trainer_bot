from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



admin_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить упражнение", callback_data="add_exercise")],
    [InlineKeyboardButton(text="Удалить упражнение", callback_data="delete_exercise"), InlineKeyboardButton(text="Изменить упражнение", callback_data="change_exercise")]
    ])
    
