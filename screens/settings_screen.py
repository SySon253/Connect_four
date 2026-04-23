# ============================================================================
# SETTINGS_SCREEN.PY - Màn hình cài đặt
# ============================================================================

import pygame
from utils.constants import *
from utils.asset_loader import asset_loader
from ui.button import Button, IconButton
from ui.label import Label
from ui.slider import Slider
from ui.color_picker import ColorPicker
from ui.panel import Panel
from core.state_manager import state_manager

TEXTS = {
    'vn': {
        'settings': 'CÀI ĐẶT',
        'language': 'Ngôn ngữ:',
        'sound': 'Âm thanh:',
        'p1_color': 'Màu Quân 1:',
        'p2_color': 'Màu Quân 2:',
        'save': 'LƯU',
        'exit': 'QUAY LẠI',
        'vn_lang': 'VN',
        'en_lang': 'EN'
    },
    'en': {
        'settings': 'SETTINGS',
        'language': 'Language:',
        'sound': 'Sound:',
        'p1_color': 'Player 1 Color:',
        'p2_color': 'Player 2 Color:',
        'save': 'SAVE',
        'exit': 'BACK',
        'vn_lang': 'VN',
        'en_lang': 'EN'
    }
}

class SettingsScreen:
    """Màn hình cài đặt"""
    
    def __init__(self):
        self.font_large = asset_loader.get_font('large')
        self.font_medium = asset_loader.get_font('medium')
        self.font_small = asset_loader.get_font('small')
        
        center_x = SCREEN_WIDTH // 2
        start_y = 100
        
        # Nút ngôn ngữ
        self.lang_vn_button = Button(center_x - 100, start_y + 45, 80, 40, 'VN', 
                                    self.font_small, bg_color=COLOR_PURPLE_LIGHT)
        self.lang_en_button = Button(center_x + 20, start_y + 45, 80, 40, 'EN',
                                    self.font_small, bg_color=(150, 100, 150))
        
        # Slider âm thanh
        self.sound_slider = Slider(center_x - 100, start_y + 135, 200, 30,
                                  min_val=0, max_val=100,
                                  initial_val=int(state_manager.get_sound_volume() * 100))
        
        # Color picker
        self.p1_color_picker = ColorPicker(center_x - 200, start_y + 260,
                                          size=40, selected_color=state_manager.get_player1_color())
        self.p2_color_picker = ColorPicker(center_x - 200, start_y + 390,
                                          size=40, selected_color=state_manager.get_player2_color())
        
        # Nút lưu và thoát
        self.save_button = Button(center_x - 150, SCREEN_HEIGHT - 100, 120, 50,
                                 TEXTS['vn']['save'], self.font_medium,
                                 bg_color=COLOR_YELLOW)
        self.back_button = Button(center_x + 30, SCREEN_HEIGHT - 100, 120, 50,
                                 TEXTS['vn']['exit'], self.font_medium,
                                 bg_color=COLOR_EXIT)
        
        self.current_language = state_manager.get_language()
        self._update_language_buttons()
    
    def _update_language_buttons(self):
        """Cập nhật màu nút ngôn ngữ"""
        if self.current_language == LANG_VN:
            self.lang_vn_button.bg_color = COLOR_BLUE_GAME
            self.lang_en_button.bg_color = (150, 100, 150)
        else:
            self.lang_vn_button.bg_color = (150, 100, 150)
            self.lang_en_button.bg_color = COLOR_BLUE_GAME
    
    def handle_events(self, events):
        """Xử lý sự kiện"""
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            
            # Chọn ngôn ngữ
            if self.lang_vn_button.handle_event(event):
                self.current_language = LANG_VN
                state_manager.set_language(LANG_VN)
                self._update_language_buttons()
            
            if self.lang_en_button.handle_event(event):
                self.current_language = LANG_EN
                state_manager.set_language(LANG_EN)
                self._update_language_buttons()
            
            # Slider âm thanh
            self.sound_slider.handle_event(event)
            sound_volume = self.sound_slider.get_value() / 100
            state_manager.set_sound_volume(sound_volume)
            asset_loader.set_volume(sound_volume)
            
            # Color picker
            self.p1_color_picker.handle_event(event)
            self.p2_color_picker.handle_event(event)
            
            # Nút Save
            if self.save_button.handle_event(event):
                state_manager.set_player1_color(self.p1_color_picker.get_selected_color())
                state_manager.set_player2_color(self.p2_color_picker.get_selected_color())
                state_manager.save_settings()
                return SCREEN_MAIN_MENU
            
            # Nút Back
            if self.back_button.handle_event(event):
                return SCREEN_MAIN_MENU
        
        return None
    
    def update(self):
        """Cập nhật trạng thái"""
        pass
    
    def draw(self, surface):
        """Vẽ màn hình"""
        # Background gradient (tím)
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            from utils.constants import COLOR_PURPLE_DARK, COLOR_PURPLE_LIGHT
            r = int(COLOR_PURPLE_DARK[0] + (COLOR_PURPLE_LIGHT[0] - COLOR_PURPLE_DARK[0]) * ratio)
            g = int(COLOR_PURPLE_DARK[1] + (COLOR_PURPLE_LIGHT[1] - COLOR_PURPLE_DARK[1]) * ratio)
            b = int(COLOR_PURPLE_DARK[2] + (COLOR_PURPLE_LIGHT[2] - COLOR_PURPLE_DARK[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        lang = self.current_language
        center_x = SCREEN_WIDTH // 2
        start_y = 100
        
        # Tiêu đề
        title = Label(center_x, 30, TEXTS[lang]['settings'],
                     self.font_large, COLOR_YELLOW, center=True)
        title.draw(surface)
        
        # Panel chính với style đẹp
        main_panel_rect = pygame.Rect(center_x - 350, start_y, 700, SCREEN_HEIGHT - start_y - 120)
        pygame.draw.rect(surface, (200, 150, 230), main_panel_rect, border_radius=20)
        pygame.draw.rect(surface, COLOR_WHITE, main_panel_rect, 3, border_radius=20)
        
        # Label ngôn ngữ
        lang_label = Label(center_x - 300, start_y + 50, TEXTS[lang]['language'],
                          self.font_medium, COLOR_BLACK)
        lang_label.draw(surface)
        
        # Nút ngôn ngữ
        pygame.draw.rect(surface, COLOR_BLUE_GAME if self.current_language == LANG_VN else (150, 100, 150),
                        self.lang_vn_button.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_WHITE, self.lang_vn_button.rect, 2, border_radius=10)
        
        pygame.draw.rect(surface, COLOR_BLUE_GAME if self.current_language == LANG_EN else (150, 100, 150),
                        self.lang_en_button.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_WHITE, self.lang_en_button.rect, 2, border_radius=10)
        
        vn_label = Label(self.lang_vn_button.rect.centerx, self.lang_vn_button.rect.centery,
                        'VN', self.font_small, COLOR_WHITE, center=True)
        vn_label.draw(surface)
        
        en_label = Label(self.lang_en_button.rect.centerx, self.lang_en_button.rect.centery,
                        'EN', self.font_small, COLOR_WHITE, center=True)
        en_label.draw(surface)
        
        # Label âm thanh
        sound_label = Label(center_x - 300, start_y + 140, TEXTS[lang]['sound'],
                           self.font_medium, COLOR_BLACK)
        sound_label.draw(surface)
        
        # Slider âm thanh
        pygame.draw.rect(surface, COLOR_GRAY, self.sound_slider.rect)
        pygame.draw.rect(surface, COLOR_BLUE_GAME, 
                        (self.sound_slider.thumb_x, self.sound_slider.rect.y,
                         self.sound_slider.thumb_width, self.sound_slider.rect.height))
        pygame.draw.rect(surface, COLOR_BLACK, self.sound_slider.rect, 2)
        volume_label = Label(self.sound_slider.rect.right + 60, self.sound_slider.rect.centery,
                             f"{self.sound_slider.get_value()}%", self.font_small,
                             COLOR_BLACK, center=True)
        volume_label.draw(surface)
        
        # Label màu quân
        p1_label = Label(center_x - 300, start_y + 215, TEXTS[lang]['p1_color'],
                        self.font_medium, COLOR_BLACK)
        p1_label.draw(surface)
        
        self.p1_color_picker.draw(surface)
        
        p2_label = Label(center_x - 300, start_y + 345, TEXTS[lang]['p2_color'],
                        self.font_medium, COLOR_BLACK)
        p2_label.draw(surface)
        
        self.p2_color_picker.draw(surface)
        
        # Nút Save và Back
        pygame.draw.rect(surface, COLOR_YELLOW, self.save_button.rect, border_radius=15)
        pygame.draw.rect(surface, COLOR_BLACK, self.save_button.rect, 2, border_radius=15)
        save_text = Label(self.save_button.rect.centerx, self.save_button.rect.centery,
                         TEXTS[lang]['save'], self.font_medium, COLOR_BLACK, center=True)
        save_text.draw(surface)
        
        pygame.draw.rect(surface, COLOR_EXIT, self.back_button.rect, border_radius=15)
        pygame.draw.rect(surface, COLOR_WHITE, self.back_button.rect, 2, border_radius=15)
        back_text = Label(self.back_button.rect.centerx, self.back_button.rect.centery,
                         TEXTS[lang]['exit'], self.font_medium, COLOR_WHITE, center=True)
        back_text.draw(surface)
