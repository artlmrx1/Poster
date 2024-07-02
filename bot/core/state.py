from aiogram.fsm.state import State, StatesGroup

class PostForm(StatesGroup):
    post = State()