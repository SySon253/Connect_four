# ============================================================================
# GAME_SCREEN.PY - Màn hình chơi game
# ============================================================================

import pygame
from utils.constants import *
from utils.asset_loader import asset_loader
from ui.button import Button, IconButton
from ui.label import Label
from ui.board_view import BoardView
from core.game_logic import ConnectFourGame
from core.ai_player import AIPlayer
from core.timer_manager import TimerManager
from core.state_manager import state_manager

TEXTS = {
    'vn': {
        'player': 'Lượt: Quân {}',
        'ai': 'AI',
        'time': 'Thời gian',
        'p1': 'Quân 1',
        'p2': 'Quân 2'
    },
    'en': {
        'player': 'Turn: Player {}',
        'ai': 'AI',
        'time': 'Time',
        'p1': 'Player 1',
        'p2': 'Player 2'
    }
}

class GameScreen:
    """Màn hình chơi game"""
    
    def __init__(self):
        self.font_large = asset_loader.get_font('large')
        self.font_medium = asset_loader.get_font('medium')
        self.font_small = asset_loader.get_font('small')
        
        # Game logic
        self.game = ConnectFourGame()
        self.board_view = BoardView()
        self.timer = TimerManager()
        
        # Lấy cấu hình từ state_manager
        self.game_mode = state_manager.get_game_mode()
        self.p1_color = state_manager.get_player1_color()
        self.p2_color = state_manager.get_player2_color()
        
        # AI
        self.ai = None
        if self.game_mode == GAME_MODE_PVC:
            self.ai = AIPlayer(difficulty=1)
        
        # Nút
        self.settings_button = IconButton(40, 20, 50)
        self.restart_button = IconButton(SCREEN_WIDTH - 120, 20, 50)
        self.exit_button = IconButton(SCREEN_WIDTH - 180, 20, 50)
        
        # Trạng thái
        self.ai_thinking = False
        self.ai_move_time = 0
        
        self.timer.start()
    
    def handle_events(self, events):
        """Xử lý sự kiện"""
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            
            # Nút settings
            if self.settings_button.handle_event(event):
                self.timer.pause()
                return SCREEN_SETTINGS
            
            # Nút restart
            if self.restart_button.handle_event(event):
                self.restart_game()
            
            # Nút exit
            if self.exit_button.handle_event(event):
                return "quit"
            
            # Click bàn cờ
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.is_game_over():
                    return SCREEN_RESULT
                
                if self.game.get_current_player() == 1 or self.game_mode == GAME_MODE_PVP:
                    col = self.board_view.get_column_from_mouse(event.pos[0])
                    if col >= 0:
                        self.game.make_move(col)
                        if self.game.is_game_over():
                            self.timer.pause()
        
        return None
    
    def update(self):
        """Cập nhật trạng thái"""
        if self.game.is_game_over():
            return
        
        # AI move
        if self.game_mode == GAME_MODE_PVC and self.game.get_current_player() == 2:
            if not self.ai_thinking:
                self.ai_thinking = True
                self.ai_move_time = pygame.time.get_ticks()
            else:
                # Chờ một chút để AI suy nghĩ
                if pygame.time.get_ticks() - self.ai_move_time > 800:
                    col = self.ai.get_move(self.game.board)
                    self.game.make_move(col)
                    self.ai_thinking = False
                    
                    if self.game.is_game_over():
                        self.timer.pause()
    
    def _draw_settings_icon(self, surface, x, y, size=15, color=COLOR_WHITE):
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
    
    def _draw_restart_icon(self, surface, x, y, size=12, color=COLOR_WHITE):
        """Vẽ icon restart (mũi tên vòng tròn đơn giản)"""
        center_x = int(x)
        center_y = int(y)
        radius = int(size)
        
        # Vẽ vòng tròn
        pygame.draw.circle(surface, color, (center_x, center_y), radius, 2)
        
        # Vẽ đơn giản: 2 đường thẳng tạo thành mũi tên ở phía dưới
        # Đường thẳng từ phía trên sang trái dưới
        pygame.draw.line(surface, color, 
                        (center_x + radius - 2, center_y - 3),
                        (center_x - 3, center_y + radius - 2), 2)
        
        # Mũi tên: 2 đường nhỏ
        pygame.draw.line(surface, color,
                        (center_x - 3, center_y + radius - 2),
                        (center_x - 2, center_y + radius - 6), 2)
        pygame.draw.line(surface, color,
                        (center_x - 3, center_y + radius - 2),
                        (center_x - 7, center_y + radius - 3), 2)
    
    def _draw_exit_icon(self, surface, x, y, size=12, color=COLOR_WHITE):
        """Vẽ icon exit (dấu X)"""
        # Vẽ dấu X
        offset = size
        pygame.draw.line(surface, color, (x - offset, y - offset), (x + offset, y + offset), 3)
        pygame.draw.line(surface, color, (x + offset, y - offset), (x - offset, y + offset), 3)

    def _draw_turn_panel(self, surface, lang, player_text, player_color):
        """Vẽ panel lượt chơi giống bố cục ảnh mẫu"""
        panel_width = 420
        panel_height = 190
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = self.board_view.board_y - panel_height - 20
        if panel_y < 10:
            panel_y = 10
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        # Nền panel chính
        panel_color = (120, 60, 190)
        pygame.draw.rect(surface, panel_color, panel_rect, border_radius=25)
        pygame.draw.rect(surface, COLOR_WHITE, panel_rect, 3, border_radius=25)

        # Thanh tiêu đề trên cùng
        title_rect = pygame.Rect(panel_x + 16, panel_y + 12, panel_width - 32, 42)
        pygame.draw.rect(surface, (80, 30, 150), title_rect, border_radius=18)
        title_label = Label(panel_x + panel_width // 2, title_rect.centery,
                            "PLAYER TURN", self.font_small, COLOR_WHITE, center=True)
        title_label.draw(surface)

        # Vòng tròn chỉ thị người chơi
        circle_center = (panel_x + panel_width // 2, panel_y + 95)
        pygame.draw.circle(surface, player_color, circle_center, 28)
        pygame.draw.circle(surface, COLOR_WHITE, circle_center, 28, 3)

        # Hiển thị lượt chơi bên dưới
        turn_text = TEXTS[lang]['player'].format(player_text)
        turn_label = Label(panel_x + panel_width // 2, panel_y + 165,
                           turn_text, self.font_medium, COLOR_WHITE, center=True)
        turn_label.draw(surface)
    
    def restart_game(self):
        """Restart trò chơi"""
        self.game.reset()
        self.timer.reset()
        self.timer.start()
        self.ai_thinking = False
    
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
        
        # Vẽ bàn cờ
        self.board_view.draw(surface, self.game.board, self.p1_color, self.p2_color)
        
        # Vẽ thông tin lượt chơi ở giữa phía trên giống bố cục mẫu
        if not self.game.is_game_over():
            current_player = self.game.get_current_player()
            if self.game_mode == GAME_MODE_PVC and current_player == 2:
                player_text = TEXTS[lang]['ai']
                player_color = self.p2_color
            else:
                player_text = f"{current_player}"
                player_color = self.p1_color if current_player == 1 else self.p2_color

            self._draw_turn_panel(surface, lang, player_text, player_color)

        # Vẽ timer
        time_text = self.timer.get_formatted_time()
        time_label = Label(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60,
                          f"{TEXTS[lang]['time']}: {time_text}",
                          self.font_medium, COLOR_YELLOW, center=True)
        time_label.draw(surface)
        
        # Vẽ nút với style đẹp
        # Settings button
        pygame.draw.rect(surface, COLOR_PURPLE_LIGHT, self.settings_button.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_WHITE, self.settings_button.rect, 2, border_radius=8)
        self._draw_settings_icon(surface, self.settings_button.rect.centerx, 
                                self.settings_button.rect.centery, size=12, color=COLOR_WHITE)
        
        # Restart button
        pygame.draw.rect(surface, COLOR_PURPLE_LIGHT, self.restart_button.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_WHITE, self.restart_button.rect, 2, border_radius=8)
        self._draw_restart_icon(surface, self.restart_button.rect.centerx, 
                               self.restart_button.rect.centery, size=10, color=COLOR_WHITE)
        
        # Exit button
        pygame.draw.rect(surface, COLOR_EXIT, self.exit_button.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_WHITE, self.exit_button.rect, 2, border_radius=8)
        self._draw_exit_icon(surface, self.exit_button.rect.centerx, 
                            self.exit_button.rect.centery, size=10, color=COLOR_WHITE)
        
        # Vẽ trợ giúp
        if not self.game.is_game_over():
            help_text = "Click cột để thả quân"
            help_label = Label(50, SCREEN_HEIGHT - 30, help_text,
                              self.font_small, COLOR_YELLOW)
            help_label.draw(surface)
