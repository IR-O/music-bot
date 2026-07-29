import os
from dotenv import load_dotenv
import sys

load_dotenv()

class Config:
    # API_ID - Must be a number
    API_ID = os.getenv("API_ID", "24208695")
    if API_ID is None:
        print("❌ API_ID not found in environment variables!")
        print("📌 Please set: heroku config:set API_ID=your_api_id")
        sys.exit(1)
    try:
        API_ID = int(API_ID)
        print(f"✅ API_ID loaded successfully")
    except ValueError:
        print(f"❌ Invalid API_ID: {API_ID} (must be a number)")
        sys.exit(1)
    
    # API_HASH - Must be a string
    API_HASH = os.getenv("API_HASH", "fa96a7eb2dffe7f4cc8ba1399b68d24d")
    if API_HASH is None:
        print("❌ API_HASH not found in environment variables!")
        print("📌 Please set: heroku config:set API_HASH=your_api_hash")
        sys.exit(1)
    print(f"✅ API_HASH loaded successfully")
    
    # BOT_TOKEN - Must be a string
    BOT_TOKEN = os.getenv("BOT_TOKEN", "6365132039:AAF48I0KgZe4cyHmhMiRx_K634u6BEKApDQ")
    if BOT_TOKEN is None:
        print("❌ BOT_TOKEN not found in environment variables!")
        print("📌 Please set: heroku config:set BOT_TOKEN=your_bot_token")
        sys.exit(1)
    print(f"✅ BOT_TOKEN loaded successfully")
    
    # SESSION_STRING - Must be a string
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFxZTcAS6lmQ586CKMgSTQtRPUBonBJoTku2NN0vecIwGtqmz4N2bls5T-F37bWuMWEkexHvNtZF0XhodZsdiC6AOmD0CNm27zFkr1M8lCm-hzoGVlZ30aAgSu786py_6brN-lc6zmnflTu7am0Kx26Nl5YwP0slTZBaA9rHnaRy4nh3BgImP2we6SHej6PoqI6o22eyguy0XdsE9q1Jw7RhCF7egNk7fwd1npi0C5FuRJa9ArmnTsfwrWoWYp79BbkC6bkUGbNJ5kO0eTdRUbnZUkl4AxsdeiH7woS_DayoNUrpYjEjPNLRPsloXKjzcV0A47S1Ue0Q9vPDqfqCrq45ef_1wAAAAFI8Y5zAA")
    if SESSION_STRING is None:
        print("❌ SESSION_STRING not found in environment variables!")
        print("📌 Please set: heroku config:set SESSION_STRING=your_session_string")
        sys.exit(1)
    print(f"✅ SESSION_STRING loaded successfully")
    
    # Static configurations
    SESSION_NAME = "my_session"
    PLAYLIST = []
    
    print("✅ All configurations loaded successfully!")
    print("="*50)
