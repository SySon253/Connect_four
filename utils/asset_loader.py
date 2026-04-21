import os
import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_SOUND_VOLUME

class AssetLoader:
    """Quản lý việc tải assets từ thư mục"""
    
    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        self.volume = DEFAULT_SOUND_VOLUME
        self.music_path = None
        self.music_loaded = False
        
    def load_image(self, name, path, width=None, height=None, fallback_color=(100, 100, 100)):
        """
        Tải ảnh từ file. Nếu không tìm thấy, tạo surface placeholder
        Args:
            name: Tên để lưu trong dict
            path: Đường dẫn đến file ảnh
            width, height: Kích thước mong muốn
            fallback_color: Màu fallback nếu ảnh không tìm thấy
        """
        try:
            if os.path.exists(path):
                image = pygame.image.load(path)
                if width and height:
                    image = pygame.transform.scale(image, (width, height))
                self.images[name] = image
                return image
        except Exception as e:
            print(f"Error loading image {name}: {e}")
        
        # Fallback: tạo surface đơn giản với màu
        if width and height:
            surface = pygame.Surface((width, height))
            surface.fill(fallback_color)
            self.images[name] = surface
            return surface
        
        # Default fallback
        surface = pygame.Surface((100, 100))
        surface.fill(fallback_color)
        self.images[name] = surface
        return surface
    
    def load_font(self, name, size, path=None):
        """
        Tải font từ file. Nếu không tìm thấy, dùng system font mặc định
        Ưu tiên system font cho hỗ trợ Unicode/Tiếng Việt tốt hơn
        """
        # Thử dùng system font trước (hỗ trợ Unicode tốt hơn)
        try:
            font = pygame.font.SysFont('calibri', size)
            self.fonts[name] = font
            return font
        except:
            pass
        
        # Thử path nếu có
        try:
            if path and os.path.exists(path):
                font = pygame.font.Font(path, size)
                self.fonts[name] = font
                return font
        except Exception as e:
            pass
        
        # Fallback: dùng Arial system font
        try:
            font = pygame.font.SysFont('arial', size)
            self.fonts[name] = font
            return font
        except:
            pass
        
        # Cuối cùng: default font
        font = pygame.font.Font(None, size)
        self.fonts[name] = font
        return font
    
    def load_sound(self, name, path, fallback=True):
        """
        Tải âm thanh từ file. Nếu không tìm thấy, ghi log warning
        """
        try:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.volume)
                self.sounds[name] = sound
                return sound
        except Exception as e:
            print(f"Error loading sound {name}: {e}")
        
        if fallback:
            # Tạo dummy sound object
            self.sounds[name] = None
        return None
    
    def load_music(self, path, loop=True):
        """Tải và phát nhạc nền"""
        try:
            if os.path.exists(path):
                if pygame.mixer.get_init() is None:
                    pygame.mixer.init()
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.volume)
                if loop:
                    pygame.mixer.music.play(-1)
                self.music_path = path
                self.music_loaded = True
                return True
        except Exception as e:
            print(f"Error loading music: {e}")
        self.music_loaded = False
        return False

    def set_volume(self, volume):
        """Đặt âm lượng cho toàn bộ âm thanh và nhạc nền"""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                try:
                    sound.set_volume(self.volume)
                except Exception:
                    pass
        if self.music_loaded:
            try:
                pygame.mixer.music.set_volume(self.volume)
            except Exception:
                pass

    def get_image(self, name):
        """Lấy ảnh đã tải"""
        return self.images.get(name)
    
    def get_font(self, name):
        """Lấy font đã tải"""
        return self.fonts.get(name, pygame.font.Font(None, 32))
    
    def get_sound(self, name):
        """Lấy âm thanh đã tải"""
        return self.sounds.get(name)
    
    def play_sound(self, name):
        """Phát âm thanh"""
        sound = self.get_sound(name)
        if sound:
            try:
                sound.play()
            except:
                pass

# Instance toàn cục
asset_loader = AssetLoader()

def init_assets():
    """Khởi tạo tất cả assets với hỗ trợ tiếng Việt"""
    if not pygame.get_init():
        pygame.init()
    if not pygame.font.get_init():
        pygame.font.init()
    if pygame.mixer.get_init() is None:
        try:
            pygame.mixer.init()
        except Exception:
            pass
    # Load fonts - sử dụng SysFont cho hỗ trợ Unicode/Tiếng Việt
    asset_loader.load_font('large', 48)
    asset_loader.load_font('medium', 32)
    asset_loader.load_font('small', 20)
    
    # Load images (fallback colors được áp dụng tự động)
    asset_loader.load_image('bg_main', 'assets/images/bg_main.png', SCREEN_WIDTH, SCREEN_HEIGHT)
    asset_loader.load_image('bg_settings', 'assets/images/bg_settings.png', SCREEN_WIDTH, SCREEN_HEIGHT)
    asset_loader.load_image('bg_game', 'assets/images/bg_game.png', SCREEN_WIDTH, SCREEN_HEIGHT)
    asset_loader.load_image('bg_result', 'assets/images/bg_result.png', SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Load background music
    asset_loader.load_music('assets/sounds/alexzavesa-calm-elegant-logo-519008.mp3')