import os
import aiohttp
import re
from typing import Union
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType
from config import Config

# API Configuration
API_URL = Config.SHRUTI_API_URL
API_KEY = Config.SHRUTI_API_KEY
DOWNLOAD_DIR = "downloads"

# Create download directory
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
    
    async def extract_video_id(self, link: str) -> str:
        """Extract video ID from YouTube URL"""
        # For youtube.com/watch?v=ID
        if "v=" in link:
            video_id = link.split("v=")[-1].split("&")[0]
            return video_id
        # For youtu.be/ID
        elif "youtu.be" in link:
            video_id = link.split("/")[-1].split("?")[0]
            return video_id
        # If just ID is given
        elif len(link) == 11:
            return link
        return None
    
    async def download_audio(self, link: str) -> tuple:
        """Download audio using ShrutiBots API"""
        video_id = await self.extract_video_id(link)
        if not video_id:
            return False, "Invalid YouTube URL"
        
        file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
        
        # Check if already downloaded
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return True, file_path
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{API_URL}/download",
                    params={
                        "url": video_id,
                        "type": "audio",
                        "api_key": API_KEY
                    },
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as resp:
                    if resp.status != 200:
                        return False, f"API Error: {resp.status}"
                    
                    with open(file_path, "wb") as f:
                        async for chunk in resp.content.iter_chunked(131072):
                            f.write(chunk)
            
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                return True, file_path
            return False, "Download failed"
            
        except Exception as e:
            return False, str(e)
    
    async def download_video(self, link: str) -> tuple:
        """Download video using ShrutiBots API"""
        video_id = await self.extract_video_id(link)
        if not video_id:
            return False, "Invalid YouTube URL"
        
        file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
        
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return True, file_path
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{API_URL}/download",
                    params={
                        "url": video_id,
                        "type": "video",
                        "api_key": API_KEY
                    },
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as resp:
                    if resp.status != 200:
                        return False, f"API Error: {resp.status}"
                    
                    with open(file_path, "wb") as f:
                        async for chunk in resp.content.iter_chunked(131072):
                            f.write(chunk)
            
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                return True, file_path
            return False, "Download failed"
            
        except Exception as e:
            return False, str(e)

    async def get_video_info(self, link: str) -> dict:
        """Get video info using yt-dlp (only for metadata)"""
        try:
            import yt_dlp
            
            video_id = await self.extract_video_id(link)
            if not video_id:
                return None
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
                if info:
                    return {
                        'title': info.get('title', 'Unknown'),
                        'duration': info.get('duration', 0),
                        'uploader': info.get('uploader', 'Unknown'),
                        'thumbnail': info.get('thumbnail', ''),
                        'url': f"https://youtube.com/watch?v={video_id}"
                    }
            return None
        except Exception as e:
            print(f"Info error: {e}")
            return None

    async def search(self, query: str) -> str:
        """Search YouTube and return first video URL"""
        try:
            import yt_dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if info and 'entries' in info and len(info['entries']) > 0:
                    return info['entries'][0]['url']
            return None
        except Exception as e:
            print(f"Search error: {e}")
            return None

YouTube = YouTubeAPI()
