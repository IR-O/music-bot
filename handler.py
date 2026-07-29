from pyrogram import Client, filters
from pyrogram.types import Message
from player import MusicPlayer

class Handler:
    def __init__(self, app, player):
        self.app = app
        self.player = player

    def register_handlers(self):
        @self.app.on_message(filters.command("play") & filters.group)
        async def play_command(client, message: Message):
            if len(message.command) < 2:
                await message.reply("❌ Please provide a song URL/name!\nUsage: /play <YouTube URL/name>")
                return

            query = " ".join(message.command[1:])
            
            # Check if it's a URL or search query
            if not query.startswith("http"):
                # Search YouTube
                query = f"ytsearch:{query}"
            
            chat_id = message.chat.id
            
            # Check if already playing
            if self.player.is_playing:
                self.player.queue.append(query)
                await message.reply(f"⏳ Added to queue: {query}")
                return
            
            await message.reply(f"🎵 Processing: {query}")
            
            # Try video first, then audio if fails
            success = await self.player.stream_video(chat_id, query)
            if not success:
                success = await self.player.stream_audio(chat_id, query)
            
            if success:
                await message.reply(f"▶️ Now Playing: {self.player.current_song}")
            else:
                await message.reply("❌ Failed to play! Check URL or try again.")

        @self.app.on_message(filters.command("stop") & filters.group)
        async def stop_command(client, message: Message):
            chat_id = message.chat.id
            success = await self.player.stop_stream(chat_id)
            if success:
                await message.reply("⏹️ Stream stopped")
            else:
                await message.reply("❌ No stream to stop")

        @self.app.on_message(filters.command("pause") & filters.group)
        async def pause_command(client, message: Message):
            chat_id = message.chat.id
            success = await self.player.pause_stream(chat_id)
            if success:
                await message.reply("⏸️ Stream paused")
            else:
                await message.reply("❌ Failed to pause")

        @self.app.on_message(filters.command("resume") & filters.group)
        async def resume_command(client, message: Message):
            chat_id = message.chat.id
            success = await self.player.resume_stream(chat_id)
            if success:
                await message.reply("▶️ Stream resumed")
            else:
                await message.reply("❌ Failed to resume")

        @self.app.on_message(filters.command("current") & filters.group)
        async def current_command(client, message: Message):
            if self.player.current_song:
                await message.reply(f"🎵 Currently Playing: {self.player.current_song}")
            else:
                await message.reply("❌ No song is playing")
