# imkaan_bot

Ushbu loyiha sizning botingizni o'rnatish va ishga tushirish uchun zaruriy qadamlarni taqdim etadi.

## Talablar

- Python 3.x
- PostgreSQL
- Telegram Bot API
- Boshqa kerakli kutubxonalar

## O'rnatish

1. **Loyihani klonlash:**

   ```bash
   git clone https://github.com/Nizomiddin-web/taxi-bot.git
   cd taxi-bot

2. **Virtual Muhit yaratish**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows

3. **Zaruriy kutubxonalarni o'rnatish:**
    ```bash
      pip install -r requirements.txt


## YANGI .env fayl yarating va quyidagi ma'lumotlarni yozing:
# ELATMA
**SMS_EMAIL**, **SMS_PASSWORD**, **PAYME_PROVIDER_TOKEN** va boshqa joylarda kerakli ma'lumotlarni o'zingizning haqiqiy hisoblaringiz bilan almashtiring.
**DB_CONNECT_URL** qismi uchun, sizning PostgreSQL ma'lumotlar bazangizga ulanish uchun to'g'ri foydalanuvchi **nomi, parol va ma'lumotlar bazasi** nomini kiriting.
**IP bo'limida serveringiz API manzilini ko'rsating**
 ```plaintext
    # Bot Admini
  ADMINS=1987938749
  
  # Eskiz account email va paroli (SMS xizmatlari uchun)
  SMS_EMAIL=your_sms_email@example.com
  SMS_PASSWORD=your_sms_password
  
  # Payme Bot orqali olingan Token
  PAYME_PROVIDER_TOKEN=your_payme_provider_token
  
  # Telegram Bot Tokeni
  BOT_TOKEN=7394814231:AAGDIqyOX8rvr-3fbZgK1UoCX7YDYSKdSC0
  
  # Yuz va Moshina Tekshiruvi uchun Kanal Id lari (Ikkala habar ham bitta kanalga ketishi uchun bir xil kanal ID qo'ying)
  SUPPORT_TEAM_GROUP_FACE=-1001864249751
  SUPPORT_TEAM_GROUP_CAR=-1001864249751
  
  # Adminlar guruhi uchun GURUH IDsi
  ADMIN_TEAM_GROUP=-1002262692489
  
  # Qoidalar va qo'llanmalar telegraph sahifasi uchun URL
  MANUAL_FAQ_URL=https://telegra.ph/Imkaan-taxi-bot--ManualFAQ-09-19
  
  
  # API bosh qismi (serverga murojaat uchun API URL)
  IP=http://127.0.0.1:8000/api/
  
  # Database ulanishi (Foydalanuvchi:Parol@Server/Database nomi)
  DB_CONNECT_URL=postgresql+psycopg2://postgres:1234@localhost:5432/test_db



 




  
  

 
