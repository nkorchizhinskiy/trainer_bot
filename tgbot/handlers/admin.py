from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo

from tgbot.states.admin import AdminStates, AddExersice, DeleteExersice, ChangeExersice
from tgbot.keyboards.keyboards.admin_menu_keyboard import admin_actions


async def admin_start(message: Message) -> None:
    """Start function for admin."""
    await message.reply("Привет, Admin, вы вошли в режим администрирования.", reply_markup=admin_actions)
    await AdminStates.admin_menu.set()


async def admin_add_exercise(message: Message, state: FSMContext) -> None:
    """Add exersice into DataBase."""
    
    current_state = await state.get_state()
    match current_state:
        case AdminStates.admin_menu.state:
            await message.answer("Введите название упражнения.")
            await AddExersice.input_exercise_name.set()

        case AddExersice.input_exercise_name.state:
            await state.update_data(exercise_name=message.text)
            await message.answer("Введите описание упражнения")
            await AddExersice.input_exercise_description.set()

        case AddExersice.input_exercise_description.state:
            await state.update_data(exercise_description=message.text)
            user_data = await state.get_data()
            await message.answer(f"Название упражнения - {user_data['exercise_name']}\n"
                                 f"Описание упражнения - {user_data['exercise_description']}\n")


async def admin_delete_exercise(message: Message) -> None:
    """Delete exersice from DataBase."""
    pass
    

async def admin_change_exercise(message: Message) -> None:
    """Change exersice in DataBase."""
    pass


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin"], state="*", role=UserRole.ADMIN)

    dp.register_message_handler(admin_add_exercise, state=[AdminStates.admin_menu,  AddExersice.input_exercise_name, AddExersice.input_exercise_description], role=UserRole.ADMIN)
    dp.register_message_handler(admin_delete_exercise, commands=["Delete exercise"], state=AdminStates.admin_menu, role=UserRole.ADMIN)
    dp.register_message_handler(admin_change_exercise, commands=["Change exercise"], state=AdminStates.admin_menu, role=UserRole.ADMIN)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
