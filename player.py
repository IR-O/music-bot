from pytgcalls import PyTgCalls, Stream
from pytgcalls.types import AudioPiped, VideoPiped
import yt_dlp
import asyncio

class MusicPlayer:
    def __init__(self, app):
        self.app = app
        self.call = PyTgCalls(app)
        self.current_song = None
        self.queue = []
        self.is_playing = False

    async def start(self):
        await self.call.start()

    async def stream_audio(self, chat_id, url):
        """Stream audio from YouTube URL"""
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
                
                await self.call.join_call(
                    chat_id,
                    AudioPiped(audio_url),
                )
                self.current_song = title
                self.is_playing = True
                return True
                
        except Exception as e:
            print(f"Error: {e}")
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
                
                await self.call.join_call(
                    chat_id,
                    VideoPiped(video_url),
                )
                self.current_song = title
                self.is_playing = True
                return True
                
        except Exception as e:
            print(f"Error: {e}")
            return False

    async def stop_stream(self, chat_id):
        """Stop current stream"""
        try:
            await self.call.leave_call(chat_id)
            self.is_playing = False
            self.current_song = None
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    async def pause_stream(self, chat_id):
        """Pause current stream"""
        try:
            await self.call.pause_stream(chat_id)
            return True
        except Exception:
            return False

    async def resume_stream(self, chat_id):
        """Resume paused stream"""
        try:
            await self.call.resume_stream(chat_id)
            return True
        except Exception:
            return False
