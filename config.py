import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "24208695"))
    API_HASH = os.getenv("API_HASH", "fa96a7eb2dffe7f4cc8ba1399b68d24d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "6365132039:AAF48I0KgZe4cyHmhMiRx_K634u6BEKApDQ")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFxZTcAS6lmQ586CKMgSTQtRPUBonBJoTku2NN0vecIwGtqmz4N2bls5T-F37bWuMWEkexHvNtZF0XhodZsdiC6AOmD0CNm27zFkr1M8lCm-hzoGVlZ30aAgSu786py_6brN-lc6zmnflTu7am0Kx26Nl5YwP0slTZBaA9rHnaRy4nh3BgImP2we6SHej6PoqI6o22eyguy0XdsE9q1Jw7RhCF7egNk7fwd1npi0C5FuRJa9ArmnTsfwrWoWYp79BbkC6bkUGbNJ5kO0eTdRUbnZUkl4AxsdeiH7woS_DayoNUrpYjEjPNLRPsloXKjzcV0A47S1Ue0Q9vPDqfqCrq45ef_1wAAAAFI8Y5zAA")  # <-- Naya add
    SESSION_NAME = "my_session"
    PLAYLIST = []
