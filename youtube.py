import asyncio
import os
import re
from typing import Union
import aiohttp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from config import Config

# API Configuration
API_URL = Config.SHRUTI_API_URL
API_KEY = Config.SHRUTI_API_KEY
DOWNLOAD_DIR = "downloads"

def time_to_seconds(time):
    """Convert time string to seconds"""
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

async def download_song(link: str) -> str:
    """Download audio using ShrutiBots API"""
    # Extract video ID
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
    if not video_id or len(video_id) < 3:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
    
    # Check if already downloaded
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/download",
                params={"url": video_id, "type": "audio", "api_key": API_KEY},
                timeout=aiohttp.ClientTimeout(total=300)
            ) as resp:
                if resp.status != 200:
                    return None
                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(131072):
                        f.write(chunk)
        
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path
        return None
    except Exception as e:
        print(f"Download error: {e}")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return None

async def download_video(link: str) -> str:
    """Download video using ShrutiBots API"""
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
    if not video_id or len(video_id) < 3:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
    
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/download",
                params={"url": video_id, "type": "video", "api_key": API_KEY},
                timeout=aiohttp.ClientTimeout(total=600)
            ) as resp:
                if resp.status != 200:
                    return None
                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(131072):
                        f.write(chunk)
        
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path
        return None
    except Exception as e:
        print(f"Download error: {e}")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return None

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset: entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def download_audio(self, link: str) -> tuple:
        """Download audio using API"""
        try:
            # Extract video ID
            video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
            if "youtu.be" in link:
                video_id = link.split("/")[-1].split("?")[0]
            
            # Download using API
            file_path = await download_song(video_id)
            if file_path:
                return True, file_path
            return False, "Download failed"
        except Exception as e:
            return False, str(e)

    async def download_video(self, link: str) -> tuple:
        """Download video using API"""
        try:
            video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
            if "youtu.be" in link:
                video_id = link.split("/")[-1].split("?")[0]
            
            file_path = await download_video(video_id)
            if file_path:
                return True, file_path
            return False, "Download failed"
        except Exception as e:
            return False, str(e)

    async def get_info(self, link: str) -> dict:
        """Get video info using API"""
        try:
            video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
            if "youtu.be" in link:
                video_id = link.split("/")[-1].split("?")[0]
            
            # For now, return basic info
            # API doesn't provide metadata directly
            return {
                "title": video_id,
                "duration": 0,
                "duration_sec": 0,
                "thumbnail": "",
                "vidid": video_id
            }
        except Exception:
            return None

YouTube = YouTubeAPI()
