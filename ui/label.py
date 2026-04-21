import pygame
from utils.constants import COLOR_BLACK

class Label:
    """Nhãn hiển thị text"""
    
    def __init__(self, x, y, text, font, color=None, center=False):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color or COLOR_BLACK
        self.center = center
        self.surface = None
        self.rect = None
        self._render()
    
    def _render(self):
        """Render text"""
        # Đảm bảo text là Unicode string
        if isinstance(self.text, bytes):
            text_to_render = self.text.decode('utf-8')
        else:
            text_to_render = str(self.text)
        
        self.surface = self.font.render(text_to_render, True, self.color)
        self.rect = self.surface.get_rect()
        
        if self.center:
            self.rect.center = (self.x, self.y)
        else:
            self.rect.topleft = (self.x, self.y)
    
    def set_text(self, text):
        """Đặt text mới"""
        self.text = text
        self._render()
    
    def set_position(self, x, y):
        """Đặt vị trí mới"""
        self.x = x
        self.y = y
        self._render()
    
    def draw(self, surface):
        """Vẽ label"""
        if self.surface:
            surface.blit(self.surface, self.rect)


class MultiLineLabel:
    """Nhãn hiển thị nhiều dòng text"""
    
    def __init__(self, x, y, text_list, font, color=None, spacing=10, center=False):
        self.x = x
        self.y = y
        self.text_list = text_list
        self.font = font
        self.color = color or COLOR_BLACK
        self.spacing = spacing
        self.center = center
        self.labels = []
        self._create_labels()
    
    def _create_labels(self):
        """Tạo các label con"""
        self.labels = []
        y_offset = self.y
        
        for text in self.text_list:
            label = Label(self.x, y_offset, text, self.font, self.color, self.center)
            self.labels.append(label)
            y_offset += self.font.get_height() + self.spacing
    
    def draw(self, surface):
        """Vẽ tất cả label"""
        for label in self.labels:
            label.draw(surface)
