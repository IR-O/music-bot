import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont

LOCAL_THUMBS = [
    "https://graph.org/file/e3fa9ab16ebefbfdd29d9.jpg",
    "https://graph.org/file/5938774f48c1f019c73f7.jpg",
    "https://graph.org/file/b13a16734bab174f58482.jpg",
    "https://graph.org/file/2deb4e5cbba862f2d5457.jpg",
]

async def generate_cover(user_name, title, views, duration, thumbnail):
    """Generate cover image"""
    try:
        if thumbnail:
            response = requests.get(thumbnail, timeout=10)
            with open("cover.jpg", "wb") as f:
                f.write(response.content)
        else:
            thumb_url = random.choice(LOCAL_THUMBS)
            response = requests.get(thumb_url)
            with open("cover.jpg", "wb") as f:
                f.write(response.content)
        
        img = Image.open("cover.jpg")
        img = img.resize((1280, 720))
        
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
            font_small = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Gradient overlay
        for i in range(100, 0, -1):
            draw.rectangle(
                [(0, 600 - i), (1280, 720)],
                fill=(0, 0, 0, int(i * 0.8))
            )
        
        draw.text((30, 600), f"🎵 {title[:50]}", fill=(255, 255, 255), font=font)
        draw.text((30, 660), f"👤 {user_name[:20]} • ⏱ {duration} • 👁 {views[:10]}", 
                  fill=(200, 200, 200), font=font_small)
        
        img.save("final.png")
        return "final.png"
        
    except Exception as e:
        print(f"Cover error: {e}")
        thumb_url = random.choice(LOCAL_THUMBS)
        response = requests.get(thumb_url)
        with open("final.png", "wb") as f:
            f.write(response.content)
        return "final.png"

def time_to_seconds(time_str):
    """Convert time string to seconds"""
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return int(parts[0])
    except:
        return 0

def convert_seconds(seconds):
    """Convert seconds to time string"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"
