import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Account (Commands handle karega - Bot Token)
    BOT_API_ID = int(os.environ.get("BOT_API_ID", 24208695))
    BOT_API_HASH = os.environ.get("BOT_API_HASH", "fa96a7eb2dffe7f4cc8ba1399b68d24d")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6365132039:AAF48I0KgZe4cyHmhMiRx_K634u6BEKApDQ")
    
    # Assistant Account (Voice chat mein play karega - User Session)
    ASSISTANT_SESSION = os.environ.get("ASSISTANT_SESSION", "BQFxZTcAS6lmQ586CKMgSTQtRPUBonBJoTku2NN0vecIwGtqmz4N2bls5T-F37bWuMWEkexHvNtZF0XhodZsdiC6AOmD0CNm27zFkr1M8lCm-hzoGVlZ30aAgSu786py_6brN-lc6zmnflTu7am0Kx26Nl5YwP0slTZBaA9rHnaRy4nh3BgImP2we6SHej6PoqI6o22eyguy0XdsE9q1Jw7RhCF7egNk7fwd1npi0C5FuRJa9ArmnTsfwrWoWYp79BbkC6bkUGbNJ5kO0eTdRUbnZUkl4AxsdeiH7woS_DayoNUrpYjEjPNLRPsloXKjzcV0A47S1Ue0Q9vPDqfqCrq45ef_1wAAAAFI8Y5zAA")
    ASSISTANT_API_ID = int(os.environ.get("ASSISTANT_API_ID", 24208695))
    ASSISTANT_API_HASH = os.environ.get("ASSISTANT_API_HASH", "fa96a7eb2dffe7f4cc8ba1399b68d24d")
    
    SESSION_NAME = "music_bot"
    PLAYLIST = []
