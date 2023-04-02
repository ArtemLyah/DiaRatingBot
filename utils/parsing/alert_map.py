from aiogram.types import BufferedInputFile
from PIL import Image
from io import BytesIO
import requests

url = "https://alerts.com.ua/map.png"
def parse_alert_map():
    source = requests.get(url)
    with BytesIO() as photo:
        image = Image.open(BytesIO(source.content))
        image.save(photo, format="webp")

        photo = BufferedInputFile(photo.getvalue(), "alert_map.webp")
        return photo