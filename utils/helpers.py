import json
import os
from utils.constants import *

SETTINGS_FILE = "settings.json"

def load_settings():
    """Tải cấu hình từ file JSON"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # Cấu hình mặc định
    return {
        'language': DEFAULT_LANGUAGE,
        'sound_volume': DEFAULT_SOUND_VOLUME,
        'player1_color': DEFAULT_P1_COLOR,
        'player2_color': DEFAULT_P2_COLOR,
    }

def save_settings(settings):
    """Lưu cấu hình vào file JSON"""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

def format_time(milliseconds):
    """Chuyển đổi milliseconds sang định dạng MM:SS"""
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def clamp(value, min_val, max_val):
    """Giới hạn giá trị trong khoảng [min_val, max_val]"""
    return max(min_val, min(value, max_val))

def is_point_in_rect(point, rect):
    """Kiểm tra xem điểm có nằm trong hình chữ nhật không"""
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh
