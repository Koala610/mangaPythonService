from aiogram.dispatcher.filters.state import StatesGroup,State

class AccStates(StatesGroup):
    login = State()
    password = State()

class BookmarkShowingStates(StatesGroup):
    in_process = State()

class SendMessageStates(StatesGroup):
    in_process = State()

class AnswerMessageStates(StatesGroup):
    in_process = State()