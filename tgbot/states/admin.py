from aiogram.dispatcher.filters.state import StatesGroup, State


class AddExersice(StatesGroup):
    """States which work with adding exrcise into DB"""
    input_exercise_name = State()
    input_exercise_description = State()


class DeleteExersice(StatesGroup):
    """ States which delete exercise from DB."""
    input_exersice_name = State()


class ChangeExersice(StatesGroup):
    """ States which delete exercise from DB."""
    input_exersice_name = State()
    input_exersice_description = State()

    
class AdminStates(StatesGroup):
    """ FSM for admin. Set states for extions."""
    admin_menu = State()


    
