import asyncio
from pyrogram import Client
from config import Config
from player import MusicPlayer
from handler import Handler

async def main():
    # Bot Account - Commands handle karega
    bot_app = Client(
        name="bot_account",
        api_id=Config.BOT_API_ID,
        api_hash=Config.BOT_API_HASH,
        bot_token=Config.BOT_TOKEN
    )
    
    # Assistant Account - Voice chat mein song play karega
    assistant_app = Client(
        name="assistant_account",
        api_id=Config.ASSISTANT_API_ID,
        api_hash=Config.ASSISTANT_API_HASH,
        session_string=Config.ASSISTANT_SESSION
    )

    player = MusicPlayer(assistant_app)
    handler = Handler(bot_app, player, assistant_app)
    handler.register_handlers()

    try:
        await assistant_app.start()
        print("🤖 Assistant started! (Voice Chat Player)")
        
        await bot_app.start()
        print("🤖 Bot started! (Command Handler)")
        
        await player.start()
        print("🎵 Music Player ready!")
        
        print("="*50)
        print("✅ Bot is running successfully!")
        print("="*50)
        
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
