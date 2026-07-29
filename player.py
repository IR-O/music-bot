import yt_dlp
import random

class MusicPlayer:
    def __init__(self, app):
        self.app = app
        self.current_song = None
        self.is_playing = False
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]

    async def play_song(self, chat_id, query):
        """Play song in voice chat"""
        try:
            # Check if it's a URL or search query
            if not query.startswith("http"):
                query = f"ytsearch:{query}"
            
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
                info = ydl.extract_info(query, download=False)
                
                if not info:
                    return False
                
                # Get audio URL
                audio_url = info.get('url')
                if not audio_url:
                    formats = info.get('formats', [])
                    for f in formats:
                        if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                            audio_url = f.get('url')
                            break
                
                if not audio_url:
                    return False
                
                title = info.get('title', 'Unknown')
                
                # Send audio to voice chat (bot account)
                await self.app.send_audio(
                    chat_id=chat_id,
                    audio=audio_url,
                    duration=info.get('duration', 0),
                    performer=info.get('uploader', 'Unknown'),
                    title=title
                )
                
                self.current_song = title
                self.is_playing = True
                return True
                
        except Exception as e:
            print(f"❌ Stream error: {e}")
            return False

    async def stop_stream(self):
        """Stop current stream"""
        self.is_playing = False
        self.current_song = None
        return True

    async def pause_stream(self):
        self.is_playing = False
        return True

    async def resume_stream(self):
        self.is_playing = True
        return True
