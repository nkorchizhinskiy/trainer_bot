from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




admin_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Меню упражнений", callback_data="exercise_menu")]
    ])

exercise_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить", callback_data="add_exercise"), (InlineKeyboardButton(text="Просмотреть", callback_data="print_exercises"))],
    [InlineKeyboardButton(text="Удалить", callback_data="delete_exercise"), InlineKeyboardButton(text="Изменить", callback_data="change_exercise")]
    ])


choice_of_change_exercise = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить название", callback_data="change_exercise_name"), InlineKeyboardButton(text="Изменить описание", callback_data="change_exercise_description")],
    ])
    
