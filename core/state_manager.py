# ============================================================================
# STATE_MANAGER.PY - Quản lý trạng thái ứng dụng toàn cục
# ============================================================================

from utils.constants import SCREEN_MAIN_MENU, GAME_MODE_PVP
from utils.helpers import load_settings, save_settings

class StateManager:
    """Quản lý trạng thái toàn ứng dụng"""
    
    def __init__(self):
        self.current_screen = SCREEN_MAIN_MENU
        self.settings = load_settings()
        self.game_mode = GAME_MODE_PVP
        self.selected_mode = None
    
    def set_screen(self, screen_name):
        """Chuyển đến màn hình khác"""
        self.current_screen = screen_name
    
    def get_current_screen(self):
        """Lấy màn hình hiện tại"""
        return self.current_screen
    
    def set_game_mode(self, mode):
        """Chọn chế độ chơi"""
        self.game_mode = mode
        self.selected_mode = mode
    
    def get_game_mode(self):
        """Lấy chế độ chơi"""
        return self.game_mode
    
    def get_settings(self):
        """Lấy cấu hình hiện tại"""
        return self.settings
    
    def update_setting(self, key, value):
        """Cập nhật một cài đặt"""
        self.settings[key] = value
    
    def save_settings(self):
        """Lưu cài đặt vào file"""
        return save_settings(self.settings)
    
    def get_language(self):
        """Lấy ngôn ngữ hiện tại"""
        return self.settings.get('language', 'vn')
    
    def set_language(self, lang):
        """Đặt ngôn ngữ"""
        self.settings['language'] = lang
    
    def get_player1_color(self):
        """Lấy màu người chơi 1"""
        return tuple(self.settings.get('player1_color', (255, 193, 7)))
    
    def get_player2_color(self):
        """Lấy màu người chơi 2"""
        return tuple(self.settings.get('player2_color', (220, 53, 69)))
    
    def set_player1_color(self, color):
        """Đặt màu người chơi 1"""
        self.settings['player1_color'] = color
    
    def set_player2_color(self, color):
        """Đặt màu người chơi 2"""
        self.settings['player2_color'] = color
    
    def get_sound_volume(self):
        """Lấy âm lượng"""
        return self.settings.get('sound_volume', 0.7)
    
    def set_sound_volume(self, volume):
        """Đặt âm lượng"""
        self.settings['sound_volume'] = max(0.0, min(1.0, volume))

# Instance toàn cục
state_manager = StateManager()
