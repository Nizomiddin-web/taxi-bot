import requests
from data.config import IP


class UserService:
    """User IP bilan ishlash uchun Service classi"""

    @classmethod
    def find_or_create(cls, tg_id):
        URL = f"{IP}/users/"
        data = {
            "telegram_id": tg_id
        }
        result = requests.post(url=URL, data=data)
        return result.json()

    @classmethod
    def get_user(cls, tg_id):
        URL = f"{IP}/users/{tg_id}"
        result = requests.get(url=URL)
        return result.json()

    @classmethod
    def get_user_with_phone(cls, phone):
        URL = f"{IP}/verify-phone/{phone}"
        result = requests.get(url=URL)
        return result.status_code

    @classmethod
    def update_user_info(cls, tg_id, first_name=None, last_name=None, phone=None, verification_code=None):
        URL = f"{IP}/users/{tg_id}/"

        # Faqat mavjud qiymatlar bo'yicha yangilash uchun data dictionary yaratish
        data = {}
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        if phone:
            country_code = phone[:4]
            data['phone_number'] = phone[4:]
            data['country_code'] = country_code
        if verification_code:
            data['verify_code'] = str(verification_code)

        # Agar yangilanish uchun hech narsa bo'lmasa, funksiyani to'xtatish
        if not data:
            return False

        # So'rovni yuborish
        result = requests.patch(url=URL, json=data)
        if result.status_code in [200, 204]:
            return True
        return False

    @classmethod
    def update_user_verify(cls, tg_id, phone, verification_code):
        URL = f"{IP}/users/{tg_id}/"
        data = {
            "phone_number": str(phone),
            "verify_code": str(verification_code)
        }
        result = requests.patch(url=URL, json=data)
        if result.status_code in [200, 204]:
            return True
        return False

    @classmethod
    def set_is_verified(cls, telegram_id, is_verified):
        URL = f"{IP}/users/{telegram_id}/"
        data = {
            "verification_status": is_verified
        }
        result = requests.patch(url=URL, json=data)
        if result.status_code in [200, 204]:
            return result
        return result


class MachineCheckService:
    """MachineCheck IP bilan ishlash uchun Service classi"""

    @classmethod
    def create(cls, telegram_id):
        URL = f"{IP}/machine-check/"
        data = {
            "user": telegram_id
        }
        result = requests.post(URL, data=data)
        return result.status_code

    @classmethod
    def get(cls, telegram_id):
        URL = f"{IP}/machine-check/get/{telegram_id}/"
        result = requests.get(URL)
        return result

    @classmethod
    def update(cls, telegram_id, status, rejection_reason=None):
        URL = f"{IP}/machine-check/update/"
        data = {
            "telegram_id": telegram_id,
            "status": status,
            "rejection_reason": rejection_reason
        }
        result = requests.patch(URL, json=data)
        return result.status_code


class FaceCheckService:
    """FaceCheck IP bilan ishlash uchun Service classi"""

    @classmethod
    def create(cls, telegram_id):
        URL = f"{IP}/face-check/"
        data = {
            "user": telegram_id
        }
        result = requests.post(URL, data=data)
        return result.status_code

    @classmethod
    def get(cls, telegram_id):
        URL = f"{IP}/face-check/get/{telegram_id}/"
        result = requests.get(URL)
        return result

    @classmethod
    def update(cls, telegram_id, status, rejection_reason=None):
        URL = f"{IP}/face-check/update/"
        data = {
            "telegram_id": telegram_id,
            "status": status,
            "rejection_reason": rejection_reason
        }
        result = requests.patch(URL, json=data)
        return result.status_code


class PaymentService:
    @classmethod
    def create(cls, telegram_id, amount_id):
        URL = f"{IP}/payments/"
        data = {
            "user": telegram_id,
            "amount": amount_id
        }
        result = requests.post(URL, data=data)
        return result

    @classmethod
    def get_history(cls, telegram_id):
        URL = f"{IP}/payments-history/{telegram_id}/"
        result = requests.get(URL)
        return result


class AmountService:
    @classmethod
    def get_amount(cls, payment_type):
        URL = f"{IP}/amounts/?type={payment_type}"
        result = requests.get(URL)
        if result.status_code == 200:
            return result.json()
        return False


class SupportRequestService:
    @staticmethod
    def get_active_request(telegram_id):
        # API orqali aktiv so'rovni olish
        response = requests.get(f'{IP}/support-requests/active/', params={'telegram_id': telegram_id})
        if response.status_code == 200:
            return response.json()  # Agar muvaffaqiyatli bo'lsa, so'rovni qaytaradi
        return None

    @classmethod
    def create(cls, telegram_id):
        URL = f"{IP}/support/create/"
        data = {
            "telegram_id": telegram_id
        }
        result = requests.post(URL, data=data)
        return result

    @classmethod
    def update(cls, id, telegram_id):
        URL = f"{IP}/support-request/{id}/update/"
        data = {
            "admin_id": telegram_id
        }
        result = requests.patch(URL, json=data)
        return result

    @classmethod
    def close_request(cls, support_request_id):
        URL = f"{IP}/support-requests/close/"
        data = {
            "support_request_id": support_request_id
        }
        return requests.post(URL, data=data)


class ChatLogService:
    @classmethod
    def create(cls, telegram_id, support_request_id, message):
        URL = f"{IP}/chatlog/create/"
        data = {
            "telegram_id": telegram_id,
            "support_request_id": support_request_id,
            "message": message
        }
        return requests.post(URL, data=data)
