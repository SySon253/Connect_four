# ============================================================================
# RESULT_SCREEN.PY - Màn hình hiển thị kết quả
# ============================================================================

import pygame
from utils.constants import *
from utils.asset_loader import asset_loader
from ui.button import Button
from ui.label import Label
from ui.panel import Panel
from core.state_manager import state_manager

TEXTS = {
    'vn': {
        'player1_win': 'QUÂN 1 THẮNG!',
        'player2_win': 'QUÂN 2 THẮNG!',
        'ai_win': 'AI THẮNG!',
        'draw': 'HÒA!',
        'time': 'Thời gian:',
        'home': 'TRANG CHỦ',
        'replay': 'CHƠI LẠI'
    },
    'en': {
        'player1_win': 'PLAYER 1 WINS!',
        'player2_win': 'PLAYER 2 WINS!',
        'ai_win': 'AI WINS!',
        'draw': 'DRAW!',
        'time': 'Time:',
        'home': 'HOME',
        'replay': 'REPLAY'
    }
}

class ResultScreen:
    """Màn hình kết quả"""
    
    def __init__(self, game, timer):
        self.game = game
        self.timer = timer
        
        self.font_large = asset_loader.get_font('large')
        self.font_medium = asset_loader.get_font('medium')
        self.font_small = asset_loader.get_font('small')
        
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Nút
        self.home_button = Button(center_x - 150, center_y + 100, 130, 50,
                                 'HOME', self.font_medium,
                                 bg_color=(50, 100, 200))
        self.replay_button = Button(center_x + 20, center_y + 100, 130, 50,
                                   'REPLAY', self.font_medium,
                                   bg_color=(50, 150, 50))
    
    def handle_events(self, events):
        """Xử lý sự kiện"""
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            
            if self.home_button.handle_event(event):
                return SCREEN_MAIN_MENU
            
            if self.replay_button.handle_event(event):
                return SCREEN_GAME
        
        return None
    
    def update(self):
        """Cập nhật trạng thái"""
        pass
    
    def get_result_text(self, lang):
        """Lấy text kết quả"""
        winner = self.game.get_winner()
        mode = state_manager.get_game_mode()
        
        if winner is None or winner == 0:
            return TEXTS[lang]['draw']
        elif winner == 1:
            return TEXTS[lang]['player1_win']
        elif winner == 2:
            if mode == GAME_MODE_PVC:
                return TEXTS[lang]['ai_win']
            else:
                return TEXTS[lang]['player2_win']
        
        return ""
    
    def draw(self, surface):
        """Vẽ màn hình"""
        # Background gradient tím
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            from utils.constants import COLOR_PURPLE_DARK, COLOR_PURPLE_LIGHT
            r = int(COLOR_PURPLE_DARK[0] + (COLOR_PURPLE_LIGHT[0] - COLOR_PURPLE_DARK[0]) * ratio)
            g = int(COLOR_PURPLE_DARK[1] + (COLOR_PURPLE_LIGHT[1] - COLOR_PURPLE_DARK[1]) * ratio)
            b = int(COLOR_PURPLE_DARK[2] + (COLOR_PURPLE_LIGHT[2] - COLOR_PURPLE_DARK[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        lang = state_manager.get_language()
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Panel kết quả với style đẹp
        result_panel_rect = pygame.Rect(center_x - 300, center_y - 150, 600, 300)
        pygame.draw.rect(surface, (200, 150, 230), result_panel_rect, border_radius=20)
        pygame.draw.rect(surface, COLOR_WHITE, result_panel_rect, 3, border_radius=20)
        
        # Text kết quả
        result_text = self.get_result_text(lang)
        result_label = Label(center_x, center_y - 80, result_text,
                            self.font_large, COLOR_YELLOW, center=True)
        result_label.draw(surface)
        
        # Timer
        time_text = f"{TEXTS[lang]['time']} {self.timer.get_formatted_time()}"
        time_label = Label(center_x, center_y + 20, time_text,
                          self.font_medium, COLOR_WHITE, center=True)
        time_label.draw(surface)
        
        # Nút Home với style
        pygame.draw.rect(surface, COLOR_BLUE_GAME, self.home_button.rect, border_radius=15)
        pygame.draw.rect(surface, COLOR_WHITE, self.home_button.rect, 2, border_radius=15)
        home_text = Label(self.home_button.rect.centerx, self.home_button.rect.centery,
                         TEXTS[lang]['home'], self.font_medium, COLOR_WHITE, center=True)
        home_text.draw(surface)
        
        # Nút Replay
        pygame.draw.rect(surface, COLOR_YELLOW, self.replay_button.rect, border_radius=15)
        pygame.draw.rect(surface, COLOR_BLACK, self.replay_button.rect, 2, border_radius=15)
        replay_text = Label(self.replay_button.rect.centerx, self.replay_button.rect.centery,
                           TEXTS[lang]['replay'], self.font_medium, COLOR_BLACK, center=True)
        replay_text.draw(surface)
