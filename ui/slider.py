import pygame
from utils.constants import COLOR_WHITE, COLOR_GRAY, COLOR_DARK_GRAY, COLOR_BLACK

class Slider:
    """Thanh trượt để chọn giá trị"""
    
    def __init__(self, x, y, width, height, min_val=0, max_val=100, initial_val=50):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.height = height
        self.dragging = False
        self.thumb_width = 20
        self._update_thumb_pos()
    
    def _update_thumb_pos(self):
        """Cập nhật vị trí thanh trượt"""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.thumb_x = self.rect.x + (self.rect.width - self.thumb_width) * ratio
    
    def _update_value(self, mouse_x):
        """Cập nhật giá trị dựa vào vị trí chuột"""
        relative_x = mouse_x - self.rect.x
        ratio = max(0, min(1, relative_x / self.rect.width))
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        self._update_thumb_pos()
    
    def handle_event(self, event):
        """Xử lý sự kiện"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            thumb_rect = pygame.Rect(self.thumb_x, self.rect.y, self.thumb_width, self.rect.height)
            if thumb_rect.collidepoint(event.pos):
                self.dragging = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])
            return True
        
        return False
    
    def get_value(self):
        """Lấy giá trị hiện tại"""
        return self.value
    
    def set_value(self, value):
        """Đặt giá trị"""
        self.value = max(self.min_val, min(self.max_val, value))
        self._update_thumb_pos()
    
    def draw(self, surface):
        """Vẽ slider"""
        # Vẽ background với màu tím
        pygame.draw.rect(surface, (150, 100, 180), self.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2, border_radius=10)
        
        # Vẽ thanh trượt (thumb) - xanh dương
        thumb_rect = pygame.Rect(self.thumb_x, self.rect.y, self.thumb_width, self.rect.height)
        pygame.draw.rect(surface, (100, 150, 220), thumb_rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BLACK, thumb_rect, 2, border_radius=8)