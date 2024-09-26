from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
mode = env.str("MODE", "development")

# MODE ga qarab tegishli .env faylni yuklaymiz
if mode == "development":
    env.read_env(".env.development")
elif mode == "production":
    env.read_env(".env.production")
else:
    raise ValueError("Noto'g'ri MODE qiymati belgilangan")

CHANNELS = []

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token

SMS_EMAIL = env.str("SMS_EMAIL")  # SMS ESKIZ SAYTIDAGI RO"YHATDAN o'tilgan  EMAIL UCHUN
SMS_PASSWORD = env.str("SMS_PASSWORD")  # ESKIZ SAYTIDAGI SMS PASSWORD UCHUN

SUPPORT_TEAM_GROUP_FACE = env.str("SUPPORT_TEAM_GROUP_FACE")  # Ko'rinish tekshiruvi Kanal id si
SUPPORT_TEAM_GROUP_CAR = env.str("SUPPORT_TEAM_GROUP_CAR")  # Moshina tekshiruvi Kanal Id si

ADMIN_TEAM_GROUP = env.str("ADMIN_TEAM_GROUP")  # Live Chat qilinadigan adminlar guruh id si
MANUAL_FAQ_URL = env.str("MANUAL_FAQ_URL")  # Telegraph da yozilgan qoidalar uchun URL

ADMINS = env.list("ADMINS")  # adminlar ro'yxati

PAYME_PROVIDER_TOKEN = env.str("PAYME_PROVIDER_TOKEN")  # To'lov tizimi uchun PAYME TOKEN

IP = env.str("IP")  # Xosting ip manzili

DB_CONNECT_URL = env.str("DB_CONNECT_URL")
