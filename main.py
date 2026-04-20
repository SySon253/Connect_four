# ============================================================================
# MAIN.PY - Entry point của ứng dụng Connect Four
# ============================================================================

import pygame
import sys
import os

# Đảm bảo UTF-8 encoding cho Python
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from utils.constants import *
from utils.asset_loader import init_assets, asset_loader
from config import screen, clock, FPS
from core.state_manager import state_manager
from core.game_logic import ConnectFourGame
from core.timer_manager import TimerManager
from screens.main_menu import MainMenu
from screens.settings_screen import SettingsScreen
from screens.game_screen import GameScreen
from screens.result_screen import ResultScreen

class App:
    """Ứng dụng chính"""
    
    def __init__(self):
        # Khởi tạo assets
        init_assets()
        asset_loader.set_volume(state_manager.get_sound_volume())
        
        # Khởi tạo các màn hình
        self.screens = {
            SCREEN_MAIN_MENU: MainMenu(),
            SCREEN_SETTINGS: SettingsScreen(),
        }
        
        self.current_game = None
        self.current_timer = None
        self.current_screen = SCREEN_MAIN_MENU
        
        self.running = True
    
    def _switch_screen(self, screen_name):
        """Chuyển sang màn hình khác"""
        if screen_name == SCREEN_GAME:
            # Tạo trò chơi mới
            self.current_game = GameScreen()
            self.current_timer = self.current_game.timer
            self.current_screen = SCREEN_GAME
        
        elif screen_name == SCREEN_RESULT:
            # Tạo màn hình kết quả
            if self.current_game:
                self.current_screen = SCREEN_RESULT
                self.current_result_screen = ResultScreen(self.current_game.game, self.current_timer)
        
        elif screen_name in self.screens:
            # Quay lại màn hình khác
            if self.current_screen == SCREEN_GAME and screen_name == SCREEN_SETTINGS:
                # Lưu trạng thái game để resume sau
                pass
            self.current_screen = screen_name
        
        elif screen_name == "quit":
            self.running = False
    
    def handle_events(self):
        """Xử lý sự kiện"""
        events = pygame.event.get()
        
        result = None
        
        if self.current_screen == SCREEN_MAIN_MENU:
            result = self.screens[SCREEN_MAIN_MENU].handle_events(events)
        
        elif self.current_screen == SCREEN_SETTINGS:
            result = self.screens[SCREEN_SETTINGS].handle_events(events)
        
        elif self.current_screen == SCREEN_GAME:
            if self.current_game:
                result = self.current_game.handle_events(events)
        
        elif self.current_screen == SCREEN_RESULT:
            if hasattr(self, 'current_result_screen'):
                result = self.current_result_screen.handle_events(events)
        
        if result:
            self._switch_screen(result)
    
    def update(self):
        """Cập nhật trạng thái"""
        if self.current_screen == SCREEN_MAIN_MENU:
            self.screens[SCREEN_MAIN_MENU].update()
        
        elif self.current_screen == SCREEN_SETTINGS:
            self.screens[SCREEN_SETTINGS].update()
        
        elif self.current_screen == SCREEN_GAME:
            if self.current_game:
                self.current_game.update()
                
                # Kiểm tra nếu game kết thúc
                if self.current_game.game.is_game_over():
                    self._switch_screen(SCREEN_RESULT)
        
        elif self.current_screen == SCREEN_RESULT:
            if hasattr(self, 'current_result_screen'):
                self.current_result_screen.update()
    
    def draw(self):
        """Vẽ màn hình"""
        screen.fill(COLOR_LIGHT_GRAY)
        
        if self.current_screen == SCREEN_MAIN_MENU:
            self.screens[SCREEN_MAIN_MENU].draw(screen)
        
        elif self.current_screen == SCREEN_SETTINGS:
            self.screens[SCREEN_SETTINGS].draw(screen)
        
        elif self.current_screen == SCREEN_GAME:
            if self.current_game:
                self.current_game.draw(screen)
        
        elif self.current_screen == SCREEN_RESULT:
            if hasattr(self, 'current_result_screen'):
                self.current_result_screen.draw(screen)
        
        pygame.display.flip()
    
    def run(self):
        """Chạy ứng dụng"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Hàm main"""
    app = App()
    app.run()

if __name__ == "__main__":
    main()
