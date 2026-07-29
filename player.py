import os
import random
from youtube import YouTube

class MusicPlayer:
    def __init__(self, assistant_app):
        self.assistant_app = assistant_app
        self.current_song = None
        self.is_playing = False

    async def start(self):
        print("✅ Music Player initialized!")

    async def play_song(self, chat_id, query):
        """Play song using ShrutiBots API"""
        try:
            # Check if it's a search query or URL
            if not query.startswith("http"):
                # For search, we need to get first result
                # Using yt-dlp for search only
                import yt_dlp
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)
                    if info and 'entries' in info and len(info['entries']) > 0:
                        video_url = info['entries'][0]['url']
                    else:
                        return False
            else:
                video_url = query

            # Download using API
            success, result = await YouTube.download_audio(video_url)
            
            if not success:
                # Try video as fallback
                success, result = await YouTube.download_video(video_url)
                if not success:
                    return False

            # Send to voice chat
            await self.assistant_app.send_audio(
                chat_id=chat_id,
                audio=result,
                title="Playing Music"
            )
            
            self.current_song = query
            self.is_playing = True
            
            # Clean up downloaded file
            try:
                os.remove(result)
            except:
                pass
                
            return True
                
        except Exception as e:
            print(f"❌ Stream error: {e}")
            return False

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
