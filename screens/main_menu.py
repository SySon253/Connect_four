# ============================================================================
# MAIN_MENU.PY - Màn hình chính
# ============================================================================

import pygame
from utils.constants import *
from utils.asset_loader import asset_loader
from ui.button import Button, IconButton
from ui.label import Label
from ui.panel import Panel
from core.state_manager import state_manager

# Từ điển dịch
TEXTS = {
    'vn': {
        'title': 'CONNECT FOUR',
        'choose_mode': 'CHỌN CHẾ ĐỘ CHƠI',
        'pvp': 'NGƯỜI VS NGƯỜI',
        'pvp_desc': '2 NGƯỜI CHƠI',
        'pvc': 'NGƯỜI VS MÁY',
        'pvc_desc': 'ĐẤU VỚI AI',
        'start': 'START',
        'exit': 'EXIT',
        'select_mode': 'Vui lòng chọn chế độ chơi'
    },
    'en': {
        'title': 'CONNECT FOUR',
        'choose_mode': 'CHOOSE GAME MODE',
        'pvp': 'PLAYER VS PLAYER',
        'pvp_desc': '2 PLAYERS',
        'pvc': 'PLAYER VS COMPUTER',
        'pvc_desc': 'VS A.I. OPPONENT',
        'start': 'START',
        'exit': 'EXIT',
        'select_mode': 'Please select a game mode'
    }
}

class MainMenu:
    """Màn hình menu chính"""
    
    def __init__(self):
        self.font_large = asset_loader.get_font('large')
        self.font_medium = asset_loader.get_font('medium')
        self.font_small = asset_loader.get_font('small')
        
        # Tạo các nút
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Nút chọn chế độ - với style card theo design
        self.pvp_button = Button(center_x - 280, center_y - 50, 240, 120, 
                                TEXTS['vn']['pvp'], self.font_medium,
                                bg_color=COLOR_PINK, text_color=COLOR_WHITE)
        self.pvc_button = Button(center_x + 40, center_y - 50, 240, 120,
                                TEXTS['vn']['pvc'], self.font_medium,
                                bg_color=COLOR_BLUE_GAME, text_color=COLOR_WHITE)
        
        # Nút hành động
        self.start_button = Button(center_x - 100, center_y + 120, 200, 70,
                                  TEXTS['vn']['start'], self.font_medium,
                                  bg_color=COLOR_YELLOW, text_color=COLOR_BLACK)
        
        # Icon settings - góc trên phải
        self.settings_button = IconButton(SCREEN_WIDTH - 70, 30, 50,
                                         bg_color=COLOR_PURPLE_LIGHT)
        
        self.selected_mode = None
        self.message = ""
        self.message_time = 0
    
    def handle_events(self, events):
        """Xử lý sự kiện"""
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            
            # Chọn chế độ
            if self.pvp_button.handle_event(event):
                self.selected_mode = GAME_MODE_PVP
            
            if self.pvc_button.handle_event(event):
                self.selected_mode = GAME_MODE_PVC
            
            # Nút Start
            if self.start_button.handle_event(event):
                if self.selected_mode:
                    state_manager.set_game_mode(self.selected_mode)
                    return SCREEN_GAME
                else:
                    lang = state_manager.get_language()
                    self.message = TEXTS[lang]['select_mode']
                    self.message_time = pygame.time.get_ticks()
            
            # Nút Settings
            if self.settings_button.handle_event(event):
                return SCREEN_SETTINGS
        
        return None
    
    def update(self):
        """Cập nhật trạng thái"""
        # Xóa message sau 3 giây
        if self.message and pygame.time.get_ticks() - self.message_time > 3000:
            self.message = ""
    
    def _draw_settings_icon(self, surface, x, y, size=25, color=COLOR_WHITE):
        """Vẽ icon cài đặt (bánh xe)"""
        import math
        
        # Tâm của bánh xe
        center_x, center_y = x, y
        
        # Vẽ tâm
        pygame.draw.circle(surface, color, (center_x, center_y), 5)
        
        # Vẽ 8 cái nút xung quanh (teeth)
        num_teeth = 8
        for i in range(num_teeth):
            angle = (i * 360 / num_teeth) * math.pi / 180
            
            # Vị trí nút ở bên ngoài
            outer_x = center_x + size * math.cos(angle)
            outer_y = center_y + size * math.sin(angle)
            
            # Vẽ nút nhỏ
            pygame.draw.circle(surface, color, (int(outer_x), int(outer_y)), 4)
        
        # Vẽ vòng tròn xung quanh
        pygame.draw.circle(surface, color, (center_x, center_y), int(size * 0.6), 2)
    
    def _draw_gradient_background(self, surface):
        """Vẽ background gradient tím"""
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(COLOR_PURPLE_DARK[0] + (COLOR_PURPLE_LIGHT[0] - COLOR_PURPLE_DARK[0]) * ratio)
            g = int(COLOR_PURPLE_DARK[1] + (COLOR_PURPLE_LIGHT[1] - COLOR_PURPLE_DARK[1]) * ratio)
            b = int(COLOR_PURPLE_DARK[2] + (COLOR_PURPLE_LIGHT[2] - COLOR_PURPLE_DARK[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def _draw_emoji_circles(self, surface):
        """Vẽ các vòng tròn icon ở trên"""
        center_x = SCREEN_WIDTH // 2
        circle_y = 70
        
        # Vẽ 4 vòng tròn với icon/chữ
        icons = ['●', '◯', '●', '◯']  # Filled và empty circles
        colors = [COLOR_YELLOW, COLOR_PINK, COLOR_YELLOW, COLOR_PINK]
        
        start_x = center_x - 120
        radius = 25
        
        for i, (icon, color) in enumerate(zip(icons, colors)):
            x = start_x + i * 80
            pygame.draw.circle(surface, color, (x, circle_y), radius)
            pygame.draw.circle(surface, COLOR_WHITE, (x, circle_y), radius, 3)
    
    def draw(self, surface):
        """Vẽ màn hình"""
        # Background gradient
        self._draw_gradient_background(surface)
        
        lang = state_manager.get_language()
        center_x = SCREEN_WIDTH // 2
        
        # Vẽ emoji circles ở trên
        self._draw_emoji_circles(surface)
        
        # Tiêu đề "CONNECT FOUR"
        title_text = TEXTS[lang]['title']
        title_surface = self.font_large.render(title_text, True, COLOR_WHITE)
        title_rect = title_surface.get_rect(center=(center_x, 130))
        surface.blit(title_surface, title_rect)
        
        # Subtitle "CHOOSE GAME MODE"
        choose_label = Label(center_x, 190, TEXTS[lang]['choose_mode'],
                            self.font_small, COLOR_WHITE, center=True)
        choose_label.draw(surface)
        
        # Vẽ card PVP - hồng
        pygame.draw.rect(surface, COLOR_PINK, self.pvp_button.rect, border_radius=20)
        pygame.draw.rect(surface, COLOR_WHITE, self.pvp_button.rect, 4, border_radius=20)
        
        # Icon PVP (P1 vs P2)
        pvp_icon = Label(self.pvp_button.rect.centerx - 50, self.pvp_button.rect.centery - 25,
                        'P1', self.font_medium, COLOR_BLACK, center=True)
        pvp_icon.draw(surface)
        
        vs_text = Label(self.pvp_button.rect.centerx, self.pvp_button.rect.centery - 25,
                       'vs', self.font_small, COLOR_WHITE, center=True)
        vs_text.draw(surface)
        
        pvp_icon2 = Label(self.pvp_button.rect.centerx + 50, self.pvp_button.rect.centery - 25,
                         'P2', self.font_medium, COLOR_BLACK, center=True)
        pvp_icon2.draw(surface)
        
        # Text PVP
        pvp_label = Label(self.pvp_button.rect.centerx, self.pvp_button.rect.centery + 10,
                         TEXTS[lang]['pvp'], self.font_small, COLOR_WHITE, center=True)
        pvp_label.draw(surface)
        
        pvp_desc = Label(self.pvp_button.rect.centerx, self.pvp_button.rect.centery + 35,
                        TEXTS[lang]['pvp_desc'], self.font_small, COLOR_WHITE, center=True)
        pvp_desc.draw(surface)
        
        # Vẽ card PVC - xanh
        pygame.draw.rect(surface, COLOR_BLUE_GAME, self.pvc_button.rect, border_radius=20)
        pygame.draw.rect(surface, COLOR_WHITE, self.pvc_button.rect, 4, border_radius=20)
        
        # Icon PVC (P1 vs AI)
        pvc_icon = Label(self.pvc_button.rect.centerx - 50, self.pvc_button.rect.centery - 25,
                        'P1', self.font_medium, COLOR_BLACK, center=True)
        pvc_icon.draw(surface)
        
        vs_text2 = Label(self.pvc_button.rect.centerx, self.pvc_button.rect.centery - 25,
                        'vs', self.font_small, COLOR_WHITE, center=True)
        vs_text2.draw(surface)
        
        pvc_icon2 = Label(self.pvc_button.rect.centerx + 50, self.pvc_button.rect.centery - 25,
                         'AI', self.font_medium, COLOR_BLACK, center=True)
        pvc_icon2.draw(surface)
        
        # Text PVC
        pvc_label = Label(self.pvc_button.rect.centerx, self.pvc_button.rect.centery + 10,
                         TEXTS[lang]['pvc'], self.font_small, COLOR_WHITE, center=True)
        pvc_label.draw(surface)
        
        pvc_desc = Label(self.pvc_button.rect.centerx, self.pvc_button.rect.centery + 35,
                        TEXTS[lang]['pvc_desc'], self.font_small, COLOR_WHITE, center=True)
        pvc_desc.draw(surface)
        
        # Highlight selected mode
        if self.selected_mode == GAME_MODE_PVP:
            pygame.draw.rect(surface, COLOR_YELLOW, self.pvp_button.rect, 6, border_radius=20)
        if self.selected_mode == GAME_MODE_PVC:
            pygame.draw.rect(surface, COLOR_YELLOW, self.pvc_button.rect, 6, border_radius=20)
        
        # Nút START - vàng sáng, to
        pygame.draw.rect(surface, COLOR_YELLOW_BRIGHT, self.start_button.rect, border_radius=25)
        pygame.draw.rect(surface, COLOR_BLACK, self.start_button.rect, 3, border_radius=25)
        
        # Shadow effect cho START
        shadow_rect = self.start_button.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(surface, COLOR_BUTTON_HOVER, shadow_rect, border_radius=25)
        
        start_label = Label(self.start_button.rect.centerx, self.start_button.rect.centery,
                    TEXTS[lang]['start'], self.font_medium, COLOR_BLACK, center=True)
        start_label.draw(surface)
        
        # Settings button - góc trên trái
        pygame.draw.rect(surface, COLOR_PURPLE_LIGHT, self.settings_button.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_WHITE, self.settings_button.rect, 2, border_radius=10)
        
        # Vẽ icon cài đặt
        self._draw_settings_icon(surface, self.settings_button.rect.centerx, 
                                self.settings_button.rect.centery, size=15, color=COLOR_WHITE)
        
        # Hiển thị message nếu có
        if self.message:
            msg_label = Label(center_x, SCREEN_HEIGHT - 50, self.message,
                            self.font_small, COLOR_YELLOW, center=True)
            msg_label.draw(surface)
