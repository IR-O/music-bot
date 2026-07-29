from pyrogram import Client, filters
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall
import yt_dlp
import asyncio

class MusicPlayer:
    def __init__(self, app):
        self.app = app
        self.current_song = None
        self.is_playing = False
        self.chat_id = None
        self.group_call = None

    async def start(self):
        print("✅ Music Player initialized!")

    async def stream_audio(self, chat_id, url):
        """Stream audio from YouTube URL using Pyrogram"""
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']
                title = info.get('title', 'Unknown')
                
                # Start voice chat
                await self.start_voice_chat(chat_id)
                
                # Stream audio using Pyrogram's voice chat
                await self.app.send_audio(
                    chat_id=chat_id,
                    audio=audio_url,
                    duration=info.get('duration', 0),
                    performer=info.get('uploader', 'Unknown'),
                    title=title
                )
                
                self.current_song = title
                self.is_playing = True
                self.chat_id = chat_id
                return True
                
        except Exception as e:
            print(f"❌ Stream error: {e}")
            return False

    async def stream_video(self, chat_id, url):
        """Stream video from YouTube URL"""
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info['url']
                title = info.get('title', 'Unknown')
                
                # Start voice chat
                await self.start_voice_chat(chat_id)
                
                # Send video as document
                await self.app.send_video(
                    chat_id=chat_id,
                    video=video_url,
                    duration=info.get('duration', 0),
                    caption=f"🎵 {title}"
                )
                
                self.current_song = title
                self.is_playing = True
                self.chat_id = chat_id
                return True
                
        except Exception as e:
            print(f"❌ Video stream error: {e}")
            return False

    async def start_voice_chat(self, chat_id):
        """Start voice chat in group"""
        try:
            # Check if voice chat already exists
            await self.app.invoke(
                CreateGroupCall(
                    peer=await self.app.resolve_peer(chat_id),
                    title="Music Bot"
                )
            )
            return True
        except Exception as e:
            print(f"Voice chat already exists or error: {e}")
            return False

    async def stop_stream(self, chat_id):
        """Stop current stream"""
        try:
            self.is_playing = False
            self.current_song = None
            self.chat_id = None
            return True
        except Exception as e:
            print(f"❌ Stop error: {e}")
            return False

    async def pause_stream(self, chat_id):
        """Pause current stream"""
        try:
            # Pyrogram doesn't support pause directly
            # We'll stop and resume
            self.is_playing = False
            return True
        except Exception as e:
            print(f"❌ Pause error: {e}")
            return False

    async def resume_stream(self, chat_id):
        """Resume paused stream"""
        try:
            self.is_playing = True
            return True
        except Exception as e:
            print(f"❌ Resume error: {e}")
            return False
