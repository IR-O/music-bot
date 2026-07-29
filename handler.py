from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import generate_cover, time_to_seconds
from queue import queue
import os

class Handler:
    def __init__(self, bot_app, player, assistant_app):
        self.bot_app = bot_app
        self.player = player
        self.assistant_app = assistant_app

    def register_handlers(self):
        
        @self.bot_app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            user = message.from_user
            await message.reply_text(
                f"🎵 **Hello {user.first_name}!**\n\n"
                "I'm a **Music Bot** for Telegram Voice Chats!\n\n"
                "**🎮 How to use:**\n"
                "1. Add me to a group\n"
                "2. Make me admin\n"
                "3. Start a voice chat\n"
                "4. Send: `/play <song name>`\n\n"
                "**📝 Commands:**\n"
                "• `/play` - Play audio\n"
                "• `/vplay` - Play video\n"
                "• `/skip` - Skip song\n"
                "• `/pause` - Pause\n"
                "• `/resume` - Resume\n"
                "• `/stop` - Stop\n"
                "• `/queue` - Show queue\n"
                "• `/volume` - Change volume\n"
                "• `/current` - Current song\n\n"
                "**👨‍💻 Developer:** @narratorxcb",
                disable_web_page_preview=True
            )

        @self.bot_app.on_message(filters.command(["play", "vplay"]) & filters.group)
        async def play_command(client, message: Message):
            is_video = message.command[0].startswith("v")
            
            if len(message.command) < 2:
                await message.reply_text(
                    "❌ **Please provide a song name!**\n\n"
                    "**Usage:** `/play <song name>`"
                )
                return

            query = " ".join(message.command[1:])
            chat_id = message.chat.id
            user_name = message.from_user.mention
            
            msg = await message.reply_text("🔍 **Searching...**")
            
            try:
                # Join voice chat
                join_success = await self.join_voice_chat(chat_id)
                if not join_success:
                    await msg.edit_text("❌ **Failed to join voice chat!**")
                    return
                
                # Play song
                if is_video:
                    success, song_info = await self.player.play_video(chat_id, query)
                else:
                    success, song_info = await self.player.play_song(chat_id, query)
                
                if success and song_info:
                    await generate_cover(
                        user_name,
                        song_info['title'],
                        song_info['views'],
                        song_info['duration'],
                        song_info['thumbnail']
                    )
                    
                    await message.reply_photo(
                        photo="final.png",
                        caption=f"**➻ Started Streaming**\n\n"
                                f"🏷️ **Name:** [{song_info['title']}]({song_info['link']})\n"
                                f"⏰ **Duration:** `{song_info['duration']}`\n"
                                f"👀 **Views:** {song_info['views']}\n"
                                f"👤 **Requested by:** {user_name}",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                             InlineKeyboardButton("⏹ Stop", callback_data="stop")],
                            [InlineKeyboardButton("❌ Close", callback_data="close_data")]
                        ])
                    )
                    
                    os.remove("final.png")
                    await msg.delete()
                    
                else:
                    await msg.edit_text("❌ **Failed to play song!**")
                    
            except Exception as e:
                await msg.edit_text(f"❌ **Error:** {str(e)[:200]}")

        @self.bot_app.on_callback_query()
        async def callback_handler(client, callback_query):
            data = callback_query.data
            
            if data == "pause":
                await self.player.pause_stream()
                await callback_query.answer("⏸️ Paused!")
                
            elif data == "resume":
                await self.player.resume_stream()
                await callback_query.answer("▶️ Resumed!")
                
            elif data == "stop":
                await self.player.stop_stream()
                await callback_query.answer("⏹️ Stopped!")
                await callback_query.message.delete()
                
            elif data == "close_data":
                await callback_query.message.delete()
                await callback_query.answer("Closed!")

        @self.bot_app.on_message(filters.command("skip") & filters.group)
        async def skip_command(client, message: Message):
            chat_id = message.chat.id
            success, next_song = await self.player.skip_song(chat_id)
            if success and next_song:
                await message.reply_text(f"⏭️ **Skipped to:** {next_song['title']}")
            else:
                await message.reply_text("⏹️ **Queue empty! Stopped.**")

        @self.bot_app.on_message(filters.command("pause") & filters.group)
        async def pause_command(client, message: Message):
            success = await self.player.pause_stream()
            if success:
                await message.reply_text(f"⏸️ **Paused by** {message.from_user.mention}")
            else:
                await message.reply_text("❌ **Nothing to pause!**")

        @self.bot_app.on_message(filters.command("resume") & filters.group)
        async def resume_command(client, message: Message):
            success = await self.player.resume_stream()
            if success:
                await message.reply_text(f"▶️ **Resumed by** {message.from_user.mention}")
            else:
                await message.reply_text("❌ **Nothing to resume!**")

        @self.bot_app.on_message(filters.command("stop") & filters.group)
        async def stop_command(client, message: Message):
            success = await self.player.stop_stream()
            if success:
                await message.reply_text(f"⏹️ **Stopped by** {message.from_user.mention}")
            else:
                await message.reply_text("❌ **Nothing to stop!**")

        @self.bot_app.on_message(filters.command("queue") & filters.group)
        async def queue_command(client, message: Message):
            chat_id = message.chat.id
            size = await queue.size(chat_id)
            if size == 0:
                await message.reply_text("📋 **Queue is empty!**")
                return
            
            queue_text = f"📋 **Queue ({size}):**\n\n"
            for i in range(min(size, 10)):
                song = await queue.get(chat_id)
                if song:
                    queue_text += f"{i+1}. 🎵 {song['info']['title'][:30]}\n"
            
            await message.reply_text(queue_text)

        @self.bot_app.on_message(filters.command("volume") & filters.group)
        async def volume_command(client, message: Message):
            if len(message.command) < 2:
                await message.reply_text("❌ **Usage:** `/volume 50`")
                return
            
            try:
                volume = int(message.command[1])
                success = await self.player.change_volume(message.chat.id, volume)
                if success:
                    await message.reply_text(f"🔊 **Volume set to {volume}%**")
                else:
                    await message.reply_text("❌ **Volume must be between 0 and 200!**")
            except:
                await message.reply_text("❌ **Invalid volume!**")

        @self.bot_app.on_message(filters.command("current") & filters.group)
        async def current_command(client, message: Message):
            if self.player.current_song:
                song = self.player.current_song
                await message.reply_text(
                    f"🎵 **Currently Playing:**\n"
                    f"🏷️ **Name:** {song['title']}\n"
                    f"⏰ **Duration:** {song['duration']}\n"
                    f"📌 **Status:** {'▶️ Playing' if self.player.is_playing else '⏸️ Paused'}"
                )
            else:
                await message.reply_text("❌ **No song is playing!**")

    async def join_voice_chat(self, chat_id):
        """Join voice chat"""
        try:
            from pyrogram.raw.functions.phone import CreateGroupCall
            
            try:
                await self.assistant_app.invoke(
                    CreateGroupCall(
                        peer=await self.assistant_app.resolve_peer(chat_id),
                        title="Music Bot 🎵"
                    )
                )
                return True
            except Exception:
                return True
                
        except Exception as e:
            print(f"Error joining voice chat: {e}")
            return False
