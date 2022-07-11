from aiogram import Dispatcher
from aiogram.dispatcher import filters
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.models.role import UserRole

from tgbot.states.admin import AdminStates, AddExersice
from tgbot.keyboards.inline_keyboards.admin_menu_inline_keyboard import admin_actions


async def admin_start(message: Message) -> None:
    """Start function for admin."""
    await message.answer(text="Привет, Admin, вы вошли в режим администрирования.", reply_markup=admin_actions)
    await AdminStates.admin_menu.set()


#<--- Add Exersice --->
async def admin_add_exercise_name(call: CallbackQuery) -> None:
    """Add exersice into DataBase."""
    await call.message.answer("Введите название упражнения.")
    await AddExersice.input_exercise_name.set()


async def admin_add_exercise_description(message: Message, state: FSMContext) -> None:
    """Add exersice into DataBase."""
    await state.update_data(exercise_name=message.text)
    await message.answer("Введите описание упражнения")
    await AddExersice.input_exercise_description.set()


async def admin_add_exercise_output_result(message: Message, state: FSMContext) -> None:
    """Add exersice into DataBase."""
    await state.update_data(exercise_description=message.text)
    user_data = await state.get_data()
    await message.answer(f"Название упражнения - {user_data['exercise_name']}\n"
                         f"Описание упражнения - {user_data['exercise_description']}\n")
    await state.finish()



async def admin_delete_exercise(message: Message) -> None:
    """Delete exersice from DataBase."""
    pass
    

async def admin_change_exercise(message: Message) -> None:
    """Change exersice in DataBase."""
    pass


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin"], state="*", role=UserRole.ADMIN)

    # Add exersice.
    dp.register_callback_query_handler(admin_add_exercise_name, text=["add_exercise"], state=AdminStates.admin_menu, role=UserRole.ADMIN)
    dp.register_message_handler(admin_add_exercise_description, state=AddExersice.input_exercise_name, role=UserRole.ADMIN)
    dp.register_message_handler(admin_add_exercise_output_result, state=AddExersice.input_exercise_description, role=UserRole.ADMIN)

    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
