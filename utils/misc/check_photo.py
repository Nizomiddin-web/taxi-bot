from PIL import Image
from PIL.ExifTags import TAGS


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
        return taken_time
    else:
        return "EXIF ma'lumotlari topilmadi."


# Rasm yo'lini kiriting
image_path = 'rasm.jpg'
time_taken = get_image_taken_time(image_path)

if time_taken:
    print(f"Rasm olingan vaqti: {time_taken}")
else:
    print("Olingan vaqt topilmadi.")
