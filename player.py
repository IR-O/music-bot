import os
import yt_dlp
import random

class MusicPlayer:
    def __init__(self, assistant_app):
        self.assistant_app = assistant_app
        self.current_song = None
        self.current_duration = 0
        self.current_uploader = None
        self.current_title = None
        self.is_playing = False
        self.current_url = None
        self.current_info = None

    async def start(self):
        print("✅ Music Player initialized!")

    async def play_song(self, chat_id, query):
        """Assistant voice chat mein song play karega"""
        try:
            # Search or direct URL
            if not query.startswith("http"):
                query = f"ytsearch:{query}"
            
            # Get video info
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web', 'ios'],
                        'skip': ['hls', 'dash'],
                    }
                },
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                
                if not info:
                    return False, None
                
                # Get audio URL
                audio_url = info.get('url')
                if not audio_url:
                    formats = info.get('formats', [])
                    for f in formats:
                        if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                            audio_url = f.get('url')
                            break
                
                if not audio_url:
                    return False, None
                
                # Extract details
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                thumbnail = info.get('thumbnail', '')
                video_url = info.get('webpage_url', '')
                
                # Save info
                self.current_song = title
                self.current_duration = duration
                self.current_uploader = uploader
                self.current_title = title
                self.current_url = video_url
                self.current_info = info
                self.is_playing = True
                
                # Assistant se audio send karo (voice chat mein play hoga)
                await self.assistant_app.send_audio(
                    chat_id=chat_id,
                    audio=audio_url,
                    duration=duration,
                    performer=uploader,
                    title=title
                )
                
                return True, {
                    'title': title,
                    'duration': duration,
                    'uploader': uploader,
                    'thumbnail': thumbnail,
                    'url': video_url
                }
                
        except Exception as e:
            print(f"❌ Stream error: {e}")
            return False, None

    async def stop_stream(self):
        self.is_playing = False
        self.current_song = None
        return True

    async def pause_stream(self):
        self.is_playing = False
        return True

    async def resume_stream(self):
        self.is_playing = True
        return True
