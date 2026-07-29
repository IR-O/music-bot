import os
import asyncio
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, VideoPiped, AudioQuality
from youtube_search import YoutubeSearch
import yt_dlp
from queue import queue

class MusicPlayer:
    def __init__(self, assistant_app):
        self.assistant_app = assistant_app
        self.call = PyTgCalls(assistant_app)
        self.current_song = {}
        self.is_playing = False
        self.current_chat_id = None
        self.volume = 100

    async def start(self):
        await self.call.start()
        print("✅ PyTgCalls started!")

    async def search_song(self, query):
        """Search song on YouTube"""
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            if results:
                duration = results[0]['duration']
                dur_sec = 0
                try:
                    parts = duration.split(':')
                    if len(parts) == 2:
                        dur_sec = int(parts[0]) * 60 + int(parts[1])
                    elif len(parts) == 3:
                        dur_sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                except:
                    dur_sec = 0
                
                return {
                    'link': f"https://youtube.com{results[0]['url_suffix']}",
                    'title': results[0]['title'],
                    'thumbnail': results[0]['thumbnails'][0],
                    'duration': duration,
                    'duration_sec': dur_sec,
                    'views': results[0]['views']
                }
            return None
        except Exception as e:
            print(f"Search error: {e}")
            return None

    async def get_audio_stream(self, link):
        """Get audio stream URL"""
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web', 'ios'],
                    }
                }
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get('url')
        except Exception as e:
            print(f"Stream error: {e}")
            return None

    async def play_song(self, chat_id, query, is_video=False):
        """Play song"""
        try:
            song_info = await self.search_song(query)
            if not song_info:
                return False, None
            
            audio_url = await self.get_audio_stream(song_info['link'])
            if not audio_url:
                return False, None
            
            # Join call
            await self.call.join_call(
                chat_id,
                AudioPiped(audio_url, AudioQuality.STUDIO)
            )
            
            self.current_song = song_info
            self.current_chat_id = chat_id
            self.is_playing = True
            
            return True, song_info
            
        except Exception as e:
            print(f"Play error: {e}")
            return False, None

    async def play_video(self, chat_id, query):
        """Play video"""
        try:
            song_info = await self.search_song(query)
            if not song_info:
                return False, None
            
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song_info['link'], download=False)
                video_url = info.get('url')
            
            if not video_url:
                return False, None
            
            await self.call.join_call(
                chat_id,
                VideoPiped(video_url)
            )
            
            self.current_song = song_info
            self.current_chat_id = chat_id
            self.is_playing = True
            
            return True, song_info
            
        except Exception as e:
            print(f"Video play error: {e}")
            return False, None

    async def stop_stream(self):
        if self.current_chat_id:
            await self.call.leave_call(self.current_chat_id)
        self.is_playing = False
        self.current_song = {}
        self.current_chat_id = None
        await queue.clear(self.current_chat_id) if self.current_chat_id else None
        return True

    async def pause_stream(self):
        if self.current_chat_id:
            await self.call.pause_stream(self.current_chat_id)
            self.is_playing = False
            return True
        return False

    async def resume_stream(self):
        if self.current_chat_id:
            await self.call.resume_stream(self.current_chat_id)
            self.is_playing = True
            return True
        return False

    async def skip_song(self, chat_id):
        next_song = await queue.get(chat_id)
        if next_song:
            await self.call.change_stream(
                chat_id,
                AudioPiped(next_song['file'], AudioQuality.STUDIO)
            )
            self.current_song = next_song['info']
            return True, next_song['info']
        else:
            await self.stop_stream()
            return False, None

    async def change_volume(self, chat_id, volume):
        if 0 <= volume <= 200:
            await self.call.change_volume_call(chat_id, volume)
            self.volume = volume
            return True
        return False
