import asyncio
from pyrogram import Client
from pytgcalls import PyTgCalls, AudioPiped
from config import Config
from player import MusicPlayer
from handler import Handler

async def main():
    # Bot Account
    bot_app = Client(
        name="bot_account",
        api_id=Config.BOT_API_ID,
        api_hash=Config.BOT_API_HASH,
        bot_token=Config.BOT_TOKEN
    )
    
    # Assistant Account
    assistant_app = Client(
        name="assistant_account",
        api_id=Config.ASSISTANT_API_ID,
        api_hash=Config.ASSISTANT_API_HASH,
        session_string=Config.ASSISTANT_SESSION
    )
    
    # PyTgCalls
    pytgcalls = PyTgCalls(assistant_app)
    
    # Player
    player = MusicPlayer(assistant_app)
    
    # Handler
    handler = Handler(bot_app, player, assistant_app, pytgcalls)
    handler.register_handlers()

    try:
        await assistant_app.start()
        print("🤖 Assistant started!")
        
        await bot_app.start()
        print("🤖 Bot started!")
        
        await pytgcalls.start()
        print("🎵 PyTgCalls started!")
        
        await player.start()
        print("✅ Music Player ready!")
        
        print("="*50)
        print("✅ Bot is running successfully!")
        print("="*50)
        
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
