import os
from youtube_api import YouTube

class MusicPlayer:
    def __init__(self, assistant_app):
        self.assistant_app = assistant_app
        self.current_song = None
        self.current_duration = 0
        self.current_uploader = None
        self.current_title = None
        self.is_playing = False
        self.current_url = None

    async def start(self):
        print("✅ Music Player initialized!")

    async def play_song(self, chat_id, query):
        """Play song using ShrutiBots API"""
        try:
            # Search if not URL
            if not query.startswith("http"):
                video_url = await YouTube.search(query)
                if not video_url:
                    return False, None
            else:
                video_url = query
            
            # Extract video ID
            video_id = await YouTube.extract_video_id(video_url)
            if not video_id:
                return False, None
            
            # Get video info
            video_info = await YouTube.get_video_info(video_id)
            
            if not video_info:
                video_info = {
                    'title': query[:50],
                    'duration': 0,
                    'uploader': 'Unknown',
                    'thumbnail': '',
                    'url': video_url
                }
            
            # Download using API
            success, result = await YouTube.download_audio(video_id)
            
            if not success:
                return False, None
            
            # Save info
            self.current_song = video_info['title']
            self.current_duration = video_info['duration']
            self.current_uploader = video_info['uploader']
            self.current_url = video_info['url']
            self.is_playing = True
            
            # Send to voice chat
            await self.assistant_app.send_audio(
                chat_id=chat_id,
                audio=result,
                duration=video_info['duration'],
                performer=video_info['uploader'],
                title=video_info['title']
            )
            
            # Clean up
            try:
                os.remove(result)
            except:
                pass
            
            return True, video_info
                
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
