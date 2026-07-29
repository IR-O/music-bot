import asyncio
from pyrogram import Client
from config import Config
from player import MusicPlayer
from handler import Handler

async def main():
    # SESSION_STRING use karein
    app = Client(
        name=Config.SESSION_NAME,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        session_string=Config.SESSION_STRING  # <-- Naya add
    )

    player = MusicPlayer(app)
    handler = Handler(app, player)
    handler.register_handlers()

    try:
        await app.start()
        print("🤖 Bot started successfully!")
        
        await player.start()
        print("🎵 Player started successfully!")
        
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
