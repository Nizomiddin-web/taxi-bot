from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime, timedelta


def get_image_taken_time(image_path):
    # Rasmdan EXIF ma'lumotlarini olish
    image = Image.open(image_path)
    exif_data = image._getexif()

    if exif_data:
        # EXIF ma'lumotlaridan kalit/qiymat juftliklarini yaratish
        exif = {
            TAGS.get(tag): value
            for tag, value in exif_data.items()
            if tag in TAGS
        }
        # Rasmning olingan vaqtini olish
        taken_time = exif.get("DateTimeOriginal")

        if taken_time:
            # Rasm vaqti 'YYYY:MM:DD HH:MM:SS' formatida bo'ladi, shuni datetime ob'ektiga aylantiramiz
            image_time = datetime.strptime(taken_time, '%Y:%m:%d %H:%M:%S')
            return image_time
        else:
            return "Olingan vaqt topilmadi."
    else:
        return "EXIF ma'lumotlari topilmadi."


def is_taken_within_last_30_minutes(image_path):
    # Rasmning olingan vaqtini olish
    taken_time = get_image_taken_time(image_path)
    if isinstance(taken_time, datetime):
        # Hozirgi vaqtni olish
        now = datetime.now()
        # Agar rasm so'nggi 30 daqiqada olingan bo'lsa
        if now - timedelta(minutes=30) <= taken_time <= now:
            return True
        else:
            return False
    else:
        # EXIF ma'lumotlari topilmagan bo'lsa, False qaytarish
        return False


