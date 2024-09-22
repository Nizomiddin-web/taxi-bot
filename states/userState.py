from aiogram.dispatcher.filters.state import State, StatesGroup


class VerificationStates(StatesGroup):
    ask_phone = State()
    generate_code = State()
    verify_code = State()


class CarCheckStates(StatesGroup):
    waiting_for_images = State()
    waiting_for_admin_decision = State()
    waiting_for_rejection_reason = State()


class FaceCheckStates(StatesGroup):
    waiting_for_images = State()
    waiting_for_admin_decision = State()
    waiting_for_rejection_reason = State()


class UpdateProfileState(StatesGroup):
    update_phone = State()
    update_first_name = State()
    update_last_name = State()


class UserState(StatesGroup):
    title = State()
    select_id = State()
    question = State()


class PersonalData(StatesGroup):
    name = State()
    email = State()
    password = State()


class GroupState(StatesGroup):
    add_group = State()
    send_group = State()
