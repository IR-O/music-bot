import os
import asyncio
from collections import deque
from utils import get_audio_stream, get_video_stream

class MusicPlayer:
    def __init__(self, assistant_app):
        self.assistant_app = assistant_app
        self.current_song = None
        self.is_playing = False
        self.queue = deque()
        self.current_chat_id = None
        self.current_info = None

    async def start(self):
        print("✅ Music Player initialized!")

    def add_to_queue(self, chat_id, file_path, song_info):
        """Add song to queue"""
        self.queue.append({
            'chat_id': chat_id,
            'file': file_path,
            'info': song_info
        })
        return len(self.queue)

    def get_next_song(self):
        """Get next song from queue"""
        if self.queue:
            return self.queue.popleft()
        return None

    def clear_queue(self):
        """Clear queue"""
        self.queue.clear()

    async def play_song(self, chat_id, query, is_video=False):
        """Play song"""
        try:
            from youtube_search import YoutubeSearch
            
            # Search if not URL
            if not query.startswith("http"):
                results = YoutubeSearch(query, max_results=1).to_dict()
                if not results:
                    return False, None
                link = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
                thumbnail = results[0]["thumbnails"][0]
                duration = results[0]["duration"]
                views = results[0]["views"]
            else:
                link = query
                title = "Unknown"
                thumbnail = None
                duration = "0:00"
                views = "0"
            
            # Get stream
            if is_video:
                file_path = await get_video_stream(link)
            else:
                file_path = await get_audio_stream(link)
            
            song_info = {
                'title': title,
                'duration': duration,
                'thumbnail': thumbnail,
                'views': views,
                'link': link
            }
            
            return True, {'file': file_path, 'info': song_info}
            
        except Exception as e:
            print(f"Error: {e}")
            return False, None

    async def stop_stream(self):
        self.is_playing = False
        self.current_song = None
        self.current_chat_id = None
        self.clear_queue()
        return True

    async def pause_stream(self):
        self.is_playing = False
        return True

    async def resume_stream(self):
        self.is_playing = True
        return True
