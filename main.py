import asyncio
from pyrogram import Client
from config import Config
from player import MusicPlayer
from handler import Handler

async def main():
    # Initialize Pyrogram client
    app = Client(
        Config.SESSION_NAME,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN
    )

    # Initialize player
    player = MusicPlayer(app)
    
    # Initialize handler
    handler = Handler(app, player)
    
    # Register handlers
    handler.register_handlers()

    try:
        # Start client
        await app.start()
        print("🤖 Bot started successfully!")
        
        # Start player
        await player.start()
        print("🎵 Player started successfully!")
        
        # Keep bot running
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
