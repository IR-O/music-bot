from pyrogram import Client
import yt_dlp
import asyncio
import random

class MusicPlayer:
    def __init__(self, app):
        self.app = app
        self.current_song = None
        self.is_playing = False
        self.chat_id = None
        
        # Multiple user agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]

    async def start(self):
        print("✅ Music Player initialized!")

    async def stream_audio(self, chat_id, url):
        """Stream audio from YouTube"""
        try:
            user_agent = random.choice(self.user_agents)
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'skip': ['hls', 'dash'],
                    }
                },
                'user_agent': user_agent,
                'headers': {
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return False
                
                # Get audio URL
                audio_url = info.get('url')
                if not audio_url:
                    # Try to get from formats
                    formats = info.get('formats', [])
                    for f in formats:
                        if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                            audio_url = f.get('url')
                            break
                
                if not audio_url:
                    return False
                
                title = info.get('title', 'Unknown')
                
                # Send audio to chat (this will play in voice chat if joined)
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
        """Stream video from YouTube"""
        try:
            user_agent = random.choice(self.user_agents)
            
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                    }
                },
                'user_agent': user_agent,
                'headers': {
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return False
                
                video_url = info.get('url')
                if not video_url:
                    # Try to get from formats
                    formats = info.get('formats', [])
                    for f in formats:
                        if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                            video_url = f.get('url')
                            break
                
                if not video_url:
                    return False
                
                title = info.get('title', 'Unknown')
                
                await self.app.send_video(
                    chat_id=chat_id,
                    video=video_url,
                    duration=info.get('duration', 0),
                    caption=f"🎵 **{title}**\n\n🎤 {info.get('uploader', 'Unknown')}"
                )
                
                self.current_song = title
                self.is_playing = True
                self.chat_id = chat_id
                return True
                
        except Exception as e:
            print(f"❌ Video stream error: {e}")
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
        self.is_playing = False
        return True

    async def resume_stream(self, chat_id):
        self.is_playing = True
        return True
