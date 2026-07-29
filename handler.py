from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

class Handler:
    def __init__(self, app, player):
        self.app = app
        self.player = player

    def register_handlers(self):
        
        # ============ START COMMAND ============
        @self.app.on_message(filters.command("start"))
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
        @self.app.on_message(filters.command("play") & filters.group)
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
                # Bot directly joins voice chat
                join_success = await self.join_voice_chat(chat_id)
                if not join_success:
                    await processing_msg.edit_text(
                        "❌ **Failed to join voice chat!**\n\n"
                        "Make sure:\n"
                        "• I'm an admin in this group\n"
                        "• Voice chat is active"
                    )
                    return
                
                # Play the song
                success = await self.player.play_song(chat_id, query)
                
                if success:
                    await processing_msg.edit_text(
                        f"🎵 **Now Playing:**\n"
                        f"🎶 `{self.player.current_song}`\n\n"
                        f"📌 **Requested by:** {message.from_user.mention}\n"
                        f"🔊 **Streaming in:** Voice Chat"
                    )
                else:
                    await processing_msg.edit_text(
                        "❌ **Failed to play!**\n\n"
                        "Possible reasons:\n"
                        "• Invalid YouTube URL\n"
                        "• YouTube is blocked\n"
                        "• Song not found\n\n"
                        "Try another song or URL."
                    )
                    
            except Exception as e:
                await processing_msg.edit_text(
                    f"❌ **Error:** {str(e)[:200]}\n\n"
                    "Please try again."
                )

        # ============ STOP COMMAND ============
        @self.app.on_message(filters.command("stop") & filters.group)
        async def stop_command(client, message: Message):
            chat_id = message.chat.id
            success = await self.player.stop_stream()
            
            if success:
                await message.reply_text("⏹️ **Stream stopped!**")
            else:
                await message.reply_text("❌ **No active stream to stop!**")

        # ============ PAUSE COMMAND ============
        @self.app.on_message(filters.command("pause") & filters.group)
        async def pause_command(client, message: Message):
            success = await self.player.pause_stream()
            if success:
                await message.reply_text("⏸️ **Stream paused!**")
            else:
                await message.reply_text("❌ **Failed to pause!**")

        # ============ RESUME COMMAND ============
        @self.app.on_message(filters.command("resume") & filters.group)
        async def resume_command(client, message: Message):
            success = await self.player.resume_stream()
            if success:
                await message.reply_text("▶️ **Stream resumed!**")
            else:
                await message.reply_text("❌ **Failed to resume!**")

        # ============ CURRENT COMMAND ============
        @self.app.on_message(filters.command("current") & filters.group)
        async def current_command(client, message: Message):
            if self.player.current_song:
                await message.reply_text(
                    f"🎵 **Currently Playing:**\n"
                    f"🎶 `{self.player.current_song}`\n\n"
                    f"📌 Status: `{'Playing' if self.player.is_playing else 'Paused'}`"
                )
            else:
                await message.reply_text("❌ **No song is currently playing!**")

    # ============ JOIN VOICE CHAT ============
    async def join_voice_chat(self, chat_id):
        """Bot joins voice chat"""
        try:
            from pyrogram.raw.functions.phone import CreateGroupCall
            
            # Try to create voice chat
            try:
                await self.app.invoke(
                    CreateGroupCall(
                        peer=await self.app.resolve_peer(chat_id),
                        title="Music Bot 🎵"
                    )
                )
                return True
            except Exception:
                # Voice chat already exists
                return True
                
        except Exception as e:
            print(f"Error joining voice chat: {e}")
            return False
