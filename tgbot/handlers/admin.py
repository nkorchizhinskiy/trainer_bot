from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.models.role import UserRole
from tgbot.states.admin import AdminStates, \
                               AddExersice, \
                               DeleteExersice, \
                               ChangeExersice
from tgbot.keyboards.inline_keyboards.admin_menu_inline_keyboard import admin_actions, \
                                                                        choice_of_change_exercise, \
                                                                        exercise_actions

from database.database_actions import connection, \
                                      add_exercise_in_list,\
                                      delete_exercise_from_list, \
                                      change_exercise_info, \
                                      print_exercise_list


async def admin_start(message: Message, state: FSMContext) -> None:
    """Start function for admin."""
    await message.answer(text="Привет, Admin, вы вошли в режим администрирования.", reply_markup=admin_actions)
    await state.finish()
    await AdminStates.exercise_menu.set()


async def admin_exercise_actions(call: CallbackQuery) -> None:
    """Set inline keyboard for exercise setting."""
    await call.message.delete_reply_markup()
    await call.message.answer(text="Вы попали в меню управления упражнениями.", reply_markup=exercise_actions)
    await call.answer()


#<--- Add Exersice --->
async def admin_add_exercise_name(call: CallbackQuery) -> None:
    """Add exersice into DataBase."""
    await call.message.delete_reply_markup()
    await call.message.answer("Введите название упражнения.")
    await AddExersice.input_exercise_name.set()
    await call.answer()


async def admin_add_exercise_description(message: Message, state: FSMContext) -> None:
    """Add exersice into DataBase."""
    await state.update_data(exercise_name=message.text)
    await message.answer("Введите описание упражнения")
    await AddExersice.input_exercise_description.set()


async def admin_add_exercise_output_result(message: Message, state: FSMContext) -> None:
    """Add exersice into DataBase."""
    await state.update_data(exercise_description=message.text)
    user_data = await state.get_data()
    add_exercise_in_list(connection, exercise_name=user_data['exercise_name'], exercise_description=user_data['exercise_description'])
    await message.answer(f"Вы добавили новое упражнение!\n"
                         f"Название упражнения - {user_data['exercise_name']}\n"
                         f"Описание упражнения - {user_data['exercise_description']}\n", reply_markup=admin_actions)
    await AdminStates.exercise_menu.set()


#<--- Delete Exercise --->
async def admin_delete_exercise(call: CallbackQuery) -> None:
    """Delete exersice from DataBase."""
    await call.message.delete_reply_markup()
    await call.message.answer("Введите /delete Название упражнения.")
    await DeleteExersice.input_exersice_name.set()
    await call.answer()
    

async def admin_delete_exercise_name(message: Message, state: FSMContext) -> None:
    """Delete exercise from DataBase"""
    exercise_name = message.get_args()
    if exercise_name:
        delete_exercise_from_list(connection=connection, exercise_name=exercise_name.strip().capitalize())
    await message.answer(text=f"Упражнение - \"{exercise_name}\" удалено!", reply_markup=admin_actions)
    await AdminStates.exercise_menu.set()


#<--- Change Exercise --->
async def admin_change_exercise(call: CallbackQuery) -> None:
    """Change exersice in DataBase."""
    await call.message.delete_reply_markup()
    await call.message.answer("Введите /change Название упражнения.")
    await ChangeExersice.choice.set()
    await call.answer()


async def admin_change_exercise_choice(message: Message, state: FSMContext) -> None:
    """Input name of exercise."""
    exercise_name = message.get_args()
    await state.update_data(exercise_name=exercise_name)
    if exercise_name:
        await message.answer("Выберите, что будете изменять.", reply_markup=choice_of_change_exercise)


async def admin_change_exercise_name(call: CallbackQuery, state: FSMContext) -> None:
    """Change exercise name"""
    await call.message.delete_reply_markup()
    await call.message.answer("Введите новое название.")
    await ChangeExersice.input_exersice_name.set()
    await state.update_data(changeable_info="name")
    await call.answer()


async def admin_change_exercise_description(call: CallbackQuery, state: FSMContext) -> None:
    """Change exercise description"""
    await call.message.delete_reply_markup()
    await call.message.answer("Введите новое описание.")
    await ChangeExersice.input_exersice_description.set()
    await state.update_data(changeable_info="description")
    await call.answer()


async def admin_change_exersice_input_new(message: Message, state: FSMContext) -> None:
    """Input new name/description"""
    await message.answer(f'Вы ввели - {message.text}', reply_markup=admin_actions)
    state_data = await state.get_data()
    print(state_data["exercise_name"], state_data["changeable_info"])
    change_exercise_info(connection, state_data["exercise_name"], message.text, state_data["changeable_info"])
    await AdminStates.exercise_menu.set()


#<--- Printing List With Exercises --->
async def admin_print_exercises_list(call: CallbackQuery) -> None:
    """Print exercise's list."""
    await call.message.delete_reply_markup()
    # Getting data from database.
    exercises = print_exercise_list(connection)    
    await call.message.answer('\n'.join(exercises), reply_markup=admin_actions)
    await call.answer() # Confirmation of delivery callback.
    await AdminStates.exercise_menu.set()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin"], state="*", role=UserRole.ADMIN)
    dp.register_callback_query_handler(admin_exercise_actions, text="exercise_menu", state=AdminStates.exercise_menu, role=UserRole.ADMIN)

    # Add exersice.
    dp.register_callback_query_handler(admin_add_exercise_name, text="add_exercise", state=AdminStates.exercise_menu, role=UserRole.ADMIN)
    dp.register_message_handler(admin_add_exercise_description, state=AddExersice.input_exercise_name, role=UserRole.ADMIN)
    dp.register_message_handler(admin_add_exercise_output_result, state=AddExersice.input_exercise_description, role=UserRole.ADMIN)

    # Delete exercise.
    dp.register_callback_query_handler(admin_delete_exercise, text="delete_exercise", state=AdminStates.exercise_menu, role=UserRole.ADMIN)
    dp.register_message_handler(admin_delete_exercise_name, commands=["delete"], state=DeleteExersice.input_exersice_name, role=UserRole.ADMIN)
    
    # Change exercise.
    dp.register_callback_query_handler(admin_change_exercise, text="change_exercise", state=AdminStates.exercise_menu, role=UserRole.ADMIN)
    dp.register_message_handler(admin_change_exercise_choice, state=ChangeExersice.choice, role=UserRole.ADMIN)
    dp.register_callback_query_handler(admin_change_exercise_name, text="change_exercise_name", state=ChangeExersice.choice, role=UserRole.ADMIN)
    dp.register_callback_query_handler(admin_change_exercise_description, text="change_exercise_description", state=ChangeExersice.choice, role=UserRole.ADMIN)
    dp.register_message_handler(admin_change_exersice_input_new, state=[ChangeExersice.input_exersice_name, ChangeExersice.input_exersice_description], role=UserRole.ADMIN)

    # Print exercises.
    dp.register_callback_query_handler(admin_print_exercises_list, text="print_exercises", state=AdminStates.exercise_menu, role=UserRole.ADMIN)







    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
