import os
from dotenv import load_dotenv
import sys

load_dotenv()

class Config:
    # API_ID - Your actual API ID
    API_ID = os.getenv("API_ID", "24208695")
    if API_ID is None or API_ID == "your_api_id":
        print("❌ API_ID not set properly! Please set: heroku config:set API_ID=24208695")
        sys.exit(1)
    try:
        API_ID = int(API_ID)
        print(f"✅ API_ID loaded: {API_ID}")
    except ValueError:
        print(f"❌ Invalid API_ID: {API_ID} (must be a number)")
        sys.exit(1)
    
    # API_HASH - Your actual API HASH
    API_HASH = os.getenv("API_HASH", "fa96a7eb2dffe7f4cc8ba1399b68d24d")
    if API_HASH is None or API_HASH == "your_api_hash":
        print("❌ API_HASH not set properly! Please set: heroku config:set API_HASH=fa96a7eb2dffe7f4cc8ba1399b68d24d")
        sys.exit(1)
    print(f"✅ API_HASH loaded")
    
    # BOT_TOKEN - Your actual Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN", "6365132039:AAF48I0KgZe4cyHmhMiRx_K634u6BEKApDQ")
    if BOT_TOKEN is None or BOT_TOKEN == "your_bot_token":
        print("❌ BOT_TOKEN not set properly! Please set: heroku config:set BOT_TOKEN=your_token")
        sys.exit(1)
    print(f"✅ BOT_TOKEN loaded")
    
    # SESSION_STRING - Your actual Session String
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFxZTcAS6lmQ586CKMgSTQtRPUBonBJoTku2NN0vecIwGtqmz4N2bls5T-F37bWuMWEkexHvNtZF0XhodZsdiC6AOmD0CNm27zFkr1M8lCm-hzoGVlZ30aAgSu786py_6brN-lc6zmnflTu7am0Kx26Nl5YwP0slTZBaA9rHnaRy4nh3BgImP2we6SHej6PoqI6o22eyguy0XdsE9q1Jw7RhCF7egNk7fwd1npi0C5FuRJa9ArmnTsfwrWoWYp79BbkC6bkUGbNJ5kO0eTdRUbnZUkl4AxsdeiH7woS_DayoNUrpYjEjPNLRPsloXKjzcV0A47S1Ue0Q9vPDqfqCrq45ef_1wAAAAFI8Y5zAA")
    if SESSION_STRING is None or SESSION_STRING == "your_session_string":
        print("❌ SESSION_STRING not set properly! Please set: heroku config:set SESSION_STRING=your_session")
        sys.exit(1)
    print(f"✅ SESSION_STRING loaded")
    
    SESSION_NAME = "my_session"
    PLAYLIST = []
    
    print("="*50)
    print("✅ All configurations loaded successfully!")
    print("="*50)
