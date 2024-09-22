from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()
CHANNELS = ['@super_bot_chanel']
# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
SUPPORT_TEAM_GROUP_FACE = env.str("SUPPORT_TEAM_GROUP_FACE")
SUPPORT_TEAM_GROUP_CAR = env.str("SUPPORT_TEAM_GROUP_CAR")
ADMIN_TEAM_GROUP = env.str("ADMIN_TEAM_GROUP")
MANUAL_FAQ_URL = env.str("MANUAL_FAQ_URL")  # Telegraph da yozilgan qoidalar uchun
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("IP")  # Xosting ip manzili
