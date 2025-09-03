#!/usr/bin/env python3

import st7789
from PIL import Image, ImageDraw, ImageFont
import time
import subprocess
import requests
import json

# Initialize display
disp = st7789.ST7789(
    height=240,
    width=240,
    rotation=90,
    port=0,
    cs=0,
    dc=9,
    backlight=13,
    
    spi_speed_hz=16 * 1000 * 1000
)

def get_ip_address():
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        return result.stdout.strip().split()[0]
    except:
        return "No IP"

def get_mopidy_status():
    try:
        payload = {'method': 'core.playback.get_state', 'jsonrpc': '2.0', 'id': 1}
        response = requests.post('http://localhost:6680/mopidy/rpc', 
                               headers={'Content-Type': 'application/json'}, 
                               data=json.dumps(payload), 
                               timeout=1)
        result = response.json()
        return result.get('result', 'stopped')
    except:
        return 'stopped'

def get_volume():
    try:
        payload = {'method': 'core.mixer.get_volume', 'jsonrpc': '2.0', 'id': 1}
        response = requests.post('http://localhost:6680/mopidy/rpc', 
                               headers={'Content-Type': 'application/json'}, 
                               data=json.dumps(payload), 
                               timeout=1)
        result = response.json()
        return result.get('result', 0) or 0
    except:
        return 0

def draw_play_icon(draw, x, y, size=20, color=(255, 255, 255)):
    """Draw play triangle icon"""
    points = [
        (x, y),
        (x + size, y + size//2),
        (x, y + size)
    ]
    draw.polygon(points, fill=color)

def draw_pause_icon(draw, x, y, size=20, color=(255, 255, 255)):
    """Draw pause bars icon"""
    bar_width = size // 3
    draw.rectangle([x, y, x + bar_width, y + size], fill=color)
    draw.rectangle([x + size - bar_width, y, x + size, y + size], fill=color)

def draw_forward_icon(draw, x, y, size=20, color=(255, 255, 255)):
    """Draw forward/next icon (two triangles)"""
    # First triangle
    points1 = [
        (x, y),
        (x + size//2, y + size//2),
        (x, y + size)
    ]
    draw.polygon(points1, fill=color)
    
    # Second triangle
    points2 = [
        (x + size//2, y),
        (x + size, y + size//2),
        (x + size//2, y + size)
    ]
    draw.polygon(points2, fill=color)

def draw_back_icon(draw, x, y, size=20, color=(255, 255, 255)):
    """Draw back/previous icon (two triangles pointing left)"""
    # First triangle (pointing left)
    points1 = [
        (x + size//2, y),
        (x, y + size//2),
        (x + size//2, y + size)
    ]
    draw.polygon(points1, fill=color)
    
    # Second triangle (pointing left)
    points2 = [
        (x + size, y),
        (x + size//2, y + size//2),
        (x + size, y + size)
    ]
    draw.polygon(points2, fill=color)

def draw_volume_icon(draw, x, y, size=16, color=(255, 255, 255)):
    """Draw speaker/volume icon"""
    # Speaker base
    draw.rectangle([x, y + size//3, x + size//3, y + 2*size//3], fill=color)
    # Speaker cone
    points = [
        (x + size//3, y + size//4),
        (x + 2*size//3, y),
        (x + 2*size//3, y + size),
        (x + size//3, y + 3*size//4)
    ]
    draw.polygon(points, fill=color)
    # Sound waves
    draw.arc([x + 3*size//4, y + size//4, x + size, y + 3*size//4], 0, 180, fill=color, width=2)

def update_display():
    # Create image
    image = Image.new("RGB", (240, 240), color=(0, 0, 0))  # Black background
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Get current status
    ip = get_ip_address()
    status = get_mopidy_status()
    volume = get_volume()
    
    # Draw IP address at top
    draw.text((10, 10), f"IP: {ip}", font=font, fill=(255, 255, 255))
    
    # Draw status
    draw.text((10, 35), f"Status: {status}", font=small_font, fill=(255, 255, 255))
    
    # Draw volume bar (centered)
    bar_width = 180
    bar_height = 20
    bar_x = (240 - bar_width) // 2
    bar_y = 70
    
    # Volume bar background
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], 
                   outline=(255, 255, 255), width=2)
    
    # Volume bar fill
    fill_width = int((volume / 100) * (bar_width - 4))
    if fill_width > 0:
        draw.rectangle([bar_x + 2, bar_y + 2, bar_x + 2 + fill_width, bar_y + bar_height - 2], 
                       fill=(0, 255, 0))
    
    # Volume percentage text
    draw.text((bar_x + bar_width//2 - 15, bar_y + 25), f"{volume}%", 
              font=small_font, fill=(255, 255, 255))
    
    # Button icons with labels
    # A button (bottom left) - Play/Pause
    if status == 'playing':
        draw_pause_icon(draw, 20, 200, 20)
    else:
        draw_play_icon(draw, 20, 200, 20)
    draw.text((45, 205), "A", font=small_font, fill=(255, 255, 255))
    
    # B button (left side, middle) - Back/Previous 
    draw_back_icon(draw, 10, 120, 20, (255, 255, 255))
    draw.text((35, 125), "B", font=small_font, fill=(255, 255, 255))
    
    # X button (bottom right) - Forward/Next
    draw_forward_icon(draw, 200, 200, 20)
    draw.text((175, 205), "X", font=small_font, fill=(255, 255, 255))
    
    # Y button (top right) - Volume
    draw_volume_icon(draw, 200, 20, 16)
    draw.text((175, 30), "Y", font=small_font, fill=(255, 255, 255))
    
    # Display the image
    disp.display(image)

if __name__ == '__main__':
    print("Starting Pirate Audio Display with Button Icons...")
    
    try:
        while True:
            update_display()
            time.sleep(2)  # Update every 2 seconds
    
    except KeyboardInterrupt:
        print("\nDisplay stopped")
        # Clear display
        image = Image.new("RGB", (240, 240), color=(0, 0, 0))
        disp.display(image)
