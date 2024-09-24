from utils.api.service import UserService
from utils.db_api.model import User, session, DemoData


class UserBotService:
    @classmethod
    def find_or_create(cls, tg_id):
        user = session.query(User).filter(User.telegram_id == str(tg_id)).first()
        if not user:
            user = User(telegram_id=str(tg_id))
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    @classmethod
    def set_lang(cls, tg_id, lang):
        user = cls.find_or_create(tg_id)
        user.lang = lang
        session.commit()

    @classmethod
    def get_lang(cls, tg_id):
        user = cls.find_or_create(tg_id)
        return user


