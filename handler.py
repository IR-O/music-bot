from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import time

class Handler:
    def __init__(self, bot_app, player, assistant_app):
        self.bot_app = bot_app
        self.player = player
        self.assistant_app = assistant_app

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
                "• `/play` - Play a song\n"
                "• `/stop` - Stop playing\n"
                "• `/pause` - Pause the song\n"
                "• `/resume` - Resume the song\n"
                "• `/current` - Current playing song\n\n"
                "**👨‍💻 Developer:** @narratorxcb",
                disable_web_page_preview=True
            )

        # ============ PLAY COMMAND ============
        @self.bot_app.on_message(filters.command("play") & filters.group)
        async def play_command(client, message: Message):
            if len(message.command) < 2:
                await message.reply_text(
                    "❌ **Please provide a song name or URL!**\n\n"
                    "**Usage:** `/play <song name or YouTube URL>`\n\n"
                    "**Examples:**\n"
                    "• `/play dil tu`\n"
                    "• `/play https://youtu.be/kyjg5kX4pT0`"
                )
                return

            query = " ".join(message.command[1:])
            chat_id = message.chat.id
            
            # Send processing message
            processing_msg = await message.reply_text(
                f"🔍 **Searching:** `{query[:50]}...`\n\n"
                "⏳ Please wait..."
            )
            
            try:
                # Join voice chat
                join_success = await self.join_voice_chat(chat_id)
                if not join_success:
                    await processing_msg.edit_text(
                        "❌ **Failed to join voice chat!**\n\n"
                        "Make sure:\n"
                        "• Assistant is an admin in this group\n"
                        "• Voice chat is active"
                    )
                    return
                
                # Play song
                success, song_info = await self.player.play_song(chat_id, query)
                
                if success and song_info:
                    await processing_msg.delete()
                    
                    # Format duration
                    duration = song_info.get('duration', 0)
                    minutes = duration // 60
                    seconds = duration % 60
                    duration_str = f"{minutes}:{seconds:02d}"
                    
                    # Create message
                    message_text = f"""
🎵 **{song_info['title'][:50]}**

👤 **Uploader:** {song_info['uploader']}
⏱ **Duration:** `{duration_str}`
📢 **Status:** `▶️ Playing`

📌 **Requested by:** {message.from_user.mention}
                    """
                    
                    await self.bot_app.send_message(
                        chat_id=chat_id,
                        text=message_text,
                        reply_markup=InlineKeyboardMarkup([
                            [
                                InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                                InlineKeyboardButton("⏹ Stop", callback_data="stop"),
                                InlineKeyboardButton("▶️ Resume", callback_data="resume")
                            ],
                            [
                                InlineKeyboardButton("🔗 Watch on YouTube", url=song_info['url'])
                            ]
                        ])
                    )
                    
                else:
                    await processing_msg.edit_text(
                        "❌ **Failed to play!**\n\n"
                        "Possible reasons:\n"
                        "• Invalid YouTube URL\n"
                        "• API Key invalid or expired\n"
                        "• Song not found\n\n"
                        "Try another song or URL."
                    )
                    
            except Exception as e:
                await processing_msg.edit_text(
                    f"❌ **Error:** {str(e)[:200]}\n\n"
                    "Please try again."
                )

        # ============ CALLBACK HANDLER ============
        @self.bot_app.on_callback_query()
        async def callback_handler(client, callback_query):
            data = callback_query.data
            chat_id = callback_query.message.chat.id
            
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

        # ============ STOP COMMAND ============
        @self.bot_app.on_message(filters.command("stop") & filters.group)
        async def stop_command(client, message: Message):
            success = await self.player.stop_stream()
            if success:
                await message.reply_text("⏹️ **Stream stopped!**")
            else:
                await message.reply_text("❌ **No active stream to stop!**")

        # ============ PAUSE COMMAND ============
        @self.bot_app.on_message(filters.command("pause") & filters.group)
        async def pause_command(client, message: Message):
            success = await self.player.pause_stream()
            if success:
                await message.reply_text("⏸️ **Stream paused!**")
            else:
                await message.reply_text("❌ **Failed to pause!**")

        # ============ RESUME COMMAND ============
        @self.bot_app.on_message(filters.command("resume") & filters.group)
        async def resume_command(client, message: Message):
            success = await self.player.resume_stream()
            if success:
                await message.reply_text("▶️ **Stream resumed!**")
            else:
                await message.reply_text("❌ **Failed to resume!**")

        # ============ CURRENT COMMAND ============
        @self.bot_app.on_message(filters.command("current") & filters.group)
        async def current_command(client, message: Message):
            if self.player.current_song:
                duration = self.player.current_duration
                minutes = duration // 60
                seconds = duration % 60
                await message.reply_text(
                    f"🎵 **Currently Playing:**\n"
                    f"🎶 `{self.player.current_song}`\n"
                    f"⏱ `{minutes}:{seconds:02d}`\n\n"
                    f"📌 Status: `{'▶️ Playing' if self.player.is_playing else '⏸️ Paused'}`"
                )
            else:
                await message.reply_text("❌ **No song is currently playing!**")

    # ============ VOICE CHAT JOIN ============
    async def join_voice_chat(self, chat_id):
        """Assistant voice chat join karega"""
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
