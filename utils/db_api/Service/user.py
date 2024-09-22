from utils.api.service import UserService
from utils.db_api.model import User, session, DemoData


# class UserService:
#     @classmethod
#     def find_or_create(cls, tg_id):
#         user = session.query(User).filter(User.telegram_id == str(tg_id)).first()
#         if not user:
#             user = User(telegram_id=str(tg_id))
#             session.add(user)
#             session.commit()
#             session.refresh(user)
#         return user
#
#     @classmethod
#     def set_first_name(cls, tg_id, first_name):
#         user = cls.find_or_create(tg_id)
#         user.first_name = first_name
#         session.commit()
#
#     @classmethod
#     def set_last_name(cls, tg_id, last_name):
#         user = cls.find_or_create(tg_id)
#         user.last_name = last_name
#         session.commit()
#
#     @classmethod
#     def set_phone_number(cls, tg_id, phone_number):
#         user = cls.find_or_create(tg_id)
#         user.phone_number = phone_number
#         session.commit()
#
#     @classmethod
#     def set_is_verified(cls, tg_id, is_verified):
#         user = cls.find_or_create(tg_id)
#         user.is_verified = is_verified
#         session.commit()
#
#     @classmethod
#     def set_verification_code(cls, tg_id, verification_code):
#         user = cls.find_or_create(tg_id)
#         user.verification_code = verification_code
#         session.commit()
#
#     @classmethod
#     def update_user_info(cls, tg_id, first_name=None, last_name=None):
#         user = cls.find_or_create(tg_id)
#         if first_name:
#             user.first_name = first_name
#         if last_name:
#             user.last_name = last_name
#         session.commit()
#
#     @classmethod
#     def update_user_verify(cls, tg_id, phone, verification_code):
#         user = cls.find_or_create(tg_id)
#         user.phone_number = phone
#         user.verification_code = verification_code
#         session.commit()


class DemoService:
    @classmethod
    def is_have_user(cls, tg_id, phone_number, verification_code):
        data = session.query(DemoData).filter(DemoData.phone_number == phone_number).first()
        is_phone = UserService.get_user_with_phone(phone=phone_number)
        if not data or is_phone == 200:
            return False
        UserService.update_user_verify(tg_id, phone_number, verification_code)
        return True
