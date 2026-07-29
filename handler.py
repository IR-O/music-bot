from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import generate_cover, time_to_seconds, convert_seconds
import os

# Keyboard
CLOSE_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("❌ Close", callback_data="close_data")]
])

class Handler:
    def __init__(self, bot_app, player, assistant_app, pytgcalls):
        self.bot_app = bot_app
        self.player = player
        self.assistant_app = assistant_app
        self.pytgcalls = pytgcalls

    def register_handlers(self):
        
        # ============ START COMMAND ============
        @self.bot_app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            user = message.from_user
            await message.reply_text(
                f"🎵 **Hello {user.first_name}!**\n\n"
                "I'm a **Music Bot** that can play songs in voice chats!\n\n"
                "**🎮 How to use:**\n"
                "1. Add me to a group\n"
                "2. Make me admin\n"
                "3. Start a voice chat\n"
                "4. Send: `/play <song name or URL>`\n\n"
                "**📝 Commands:**\n"
                "• `/play` - Play audio\n"
                "• `/vplay` - Play video\n"
                "• `/skip` - Skip song\n"
                "• `/pause` - Pause\n"
                "• `/resume` - Resume\n"
                "• `/stop` - Stop\n"
                "• `/queue` - Show queue\n\n"
                "**👨‍💻 Developer:** @narratorxcb",
                disable_web_page_preview=True
            )

        # ============ PLAY COMMAND ============
        @self.bot_app.on_message(filters.command(["play", "vplay"]))
        async def play_command(client, message: Message):
            is_video = message.command[0].startswith("v")
            
            if len(message.command) < 2:
                await message.reply_text(
                    "❌ **Please provide a song name or URL!**\n\n"
                    "**Usage:** `/play <song name or YouTube URL>`"
                )
                return

            query = " ".join(message.command[1:])
            chat_id = message.chat.id
            user_name = message.from_user.mention
            
            # Send processing message
            msg = await message.reply_text("🔍 **Searching...**")
            
            try:
                # Check if assistant is in group
                try:
                    await self.assistant_app.get_chat_member(chat_id, "me")
                except:
                    try:
                        invitelink = await self.bot_app.export_chat_invite_link(chat_id)
                        await self.assistant_app.join_chat(invitelink)
                    except Exception as e:
                        await msg.edit_text(f"❌ **Error:** {str(e)[:200]}")
                        return
                
                # Play song
                success, song_data = await self.player.play_song(chat_id, query, is_video)
                
                if not success:
                    await msg.edit_text("❌ **Failed to play!**")
                    return
                
                file_path = song_data['file']
                song_info = song_data['info']
                
                # Generate cover
                await generate_cover(
                    user_name,
                    song_info['title'],
                    song_info['views'],
                    song_info['duration'],
                    song_info['thumbnail']
                )
                
                # Check if already playing
                active_calls = []
                for call in self.pytgcalls.active_calls:
                    active_calls.append(int(call.chat_id))
                
                if int(chat_id) in active_calls:
                    # Add to queue
                    position = self.player.add_to_queue(chat_id, file_path, song_info)
                    await message.reply_photo(
                        photo="final.png",
                        caption=f"**➻ Track Added To Queue » {position}**\n\n"
                                f"🏷️ **Name:** [{song_info['title'][:15]}]({song_info['link']})\n"
                                f"⏰ **Duration:** `{song_info['duration']}`\n"
                                f"👤 **Requested by:** {user_name}",
                        reply_markup=CLOSE_KEYBOARD
                    )
                else:
                    # Play now
                    await self.pytgcalls.join_group_call(
                        chat_id,
                        AudioPiped(file_path)
                    )
                    self.player.current_song = song_info
                    self.player.current_chat_id = chat_id
                    
                    await message.reply_photo(
                        photo="final.png",
                        caption=f"**➻ Started Streaming**\n\n"
                                f"🏷️ **Name:** [{song_info['title'][:15]}]({song_info['link']})\n"
                                f"⏰ **Duration:** `{song_info['duration']}`\n"
                                f"👤 **Requested by:** {user_name}",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                             InlineKeyboardButton("⏹ Stop", callback_data="stop")],
                            [InlineKeyboardButton("❌ Close", callback_data="close_data")]
                        ])
                    )
                
                # Cleanup
                os.remove("final.png")
                await msg.delete()
                
            except Exception as e:
                await msg.edit_text(f"❌ **Error:** {str(e)[:200]}")

        # ============ CALLBACK HANDLER ============
        @self.bot_app.on_callback_query()
        async def callback_handler(client, callback_query):
            data = callback_query.data
            chat_id = callback_query.message.chat.id
            
            if data == "pause":
                await self.pytgcalls.pause_stream(chat_id)
                await callback_query.answer("⏸️ Paused!")
                
            elif data == "resume":
                await self.pytgcalls.resume_stream(chat_id)
                await callback_query.answer("▶️ Resumed!")
                
            elif data == "stop":
                await self.pytgcalls.leave_group_call(chat_id)
                self.player.current_song = None
                await callback_query.answer("⏹️ Stopped!")
                await callback_query.message.delete()
                
            elif data == "close_data":
                await callback_query.message.delete()
                await callback_query.answer("Closed!")

        # ============ SKIP COMMAND ============
        @self.bot_app.on_message(filters.command("skip"))
        async def skip_command(client, message: Message):
            chat_id = message.chat.id
            
            active_calls = []
            for call in self.pytgcalls.active_calls:
                active_calls.append(int(call.chat_id))
            
            if chat_id not in active_calls:
                await message.reply_text("❌ **Nothing is playing!**")
                return
            
            # Get next song
            next_song = self.player.get_next_song()
            if next_song:
                await self.pytgcalls.change_stream(
                    chat_id,
                    AudioPiped(next_song['file'])
                )
                self.player.current_song = next_song['info']
                await message.reply_text("⏭️ **Skipped to next song!**")
            else:
                await self.pytgcalls.leave_group_call(chat_id)
                self.player.current_song = None
                await message.reply_text("⏹️ **Queue empty! Stopped.**")

        # ============ PAUSE COMMAND ============
        @self.bot_app.on_message(filters.command("pause"))
        async def pause_command(client, message: Message):
            chat_id = message.chat.id
            active_calls = []
            for call in self.pytgcalls.active_calls:
                active_calls.append(int(call.chat_id))
            
            if chat_id in active_calls:
                await self.pytgcalls.pause_stream(chat_id)
                await message.reply_text(f"⏸️ **Paused by** {message.from_user.mention}")
            else:
                await message.reply_text("❌ **No music playing!**")

        # ============ RESUME COMMAND ============
        @self.bot_app.on_message(filters.command("resume"))
        async def resume_command(client, message: Message):
            chat_id = message.chat.id
            active_calls = []
            for call in self.pytgcalls.active_calls:
                active_calls.append(int(call.chat_id))
            
            if chat_id in active_calls:
                await self.pytgcalls.resume_stream(chat_id)
                await message.reply_text(f"▶️ **Resumed by** {message.from_user.mention}")
            else:
                await message.reply_text("❌ **No music playing!**")

        # ============ STOP COMMAND ============
        @self.bot_app.on_message(filters.command("stop"))
        async def stop_command(client, message: Message):
            chat_id = message.chat.id
            active_calls = []
            for call in self.pytgcalls.active_calls:
                active_calls.append(int(call.chat_id))
            
            if chat_id in active_calls:
                await self.pytgcalls.leave_group_call(chat_id)
                self.player.current_song = None
                await message.reply_text(f"⏹️ **Stopped by** {message.from_user.mention}")
            else:
                await message.reply_text("❌ **No music playing!**")

        # ============ QUEUE COMMAND ============
        @self.bot_app.on_message(filters.command("queue"))
        async def queue_command(client, message: Message):
            if not self.player.queue:
                await message.reply_text("📋 **Queue is empty!**")
                return
            
            queue_text = "📋 **Current Queue:**\n\n"
            for i, song in enumerate(self.player.queue, 1):
                queue_text += f"{i}. 🎵 {song['info']['title'][:30]}\n"
            
            await message.reply_text(queue_text)
