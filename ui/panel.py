import pygame
from utils.constants import COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, COLOR_LIGHT_GRAY

class Panel:
    """Một khung (panel) để chứa các thành phần khác"""
    
    def __init__(self, x, y, width, height, bg_color=None, border_color=None, border_width=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color or COLOR_LIGHT_GRAY
        self.border_color = border_color or COLOR_BLACK
        self.border_width = border_width
    
    def draw(self, surface):
        """Vẽ panel"""
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
    
    def get_rect(self):
        """Lấy rect của panel"""
        return self.rect


class RoundPanel(Panel):
    """Panel với góc bo tròn"""
    
    def __init__(self, x, y, width, height, radius=10, bg_color=None, border_color=None, border_width=2):
        super().__init__(x, y, width, height, bg_color, border_color, border_width)
        self.radius = radius
    
    def draw(self, surface):
        """Vẽ panel với góc bo tròn"""
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.radius)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width, border_radius=self.radius)