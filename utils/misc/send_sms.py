from eskiz.client.sync import ClientSync

from data.config import SMS_EMAIL, SMS_PASSWORD


def send_sms(phone_number, message):
    eskiz_client = ClientSync(
        email=SMS_EMAIL,
        password=SMS_PASSWORD,
    )
    resp = eskiz_client.send_sms(
        phone_number=phone_number,
        message=message
    )
    return resp

