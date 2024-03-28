from PIL import Image
from pytesseract import image_to_string
import requests
import logging


def image_to_text(url):
    try:
        raw_image = Image.open(requests.get(url, stream=True).raw)
        text = image_to_string(raw_image)
        return text
    except Exception as e:
        logging.error(e)


