import pygame
from utils.constants import COLOR_WHITE, COLOR_GRAY, COLOR_DARK_GRAY, COLOR_BLACK

class Button:
    """Nút bấm"""
    
    def __init__(self, x, y, width, height, text, font, bg_color=None, text_color=None, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color or COLOR_GRAY
        self.text_color = text_color or COLOR_BLACK
        self.hover_color = hover_color or COLOR_DARK_GRAY
        self.is_hovered = False
        self.is_pressed = False
    
    def handle_event(self, event):
        """Xử lý sự kiện chuột"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_pressed = False
        
        return False
    
    def draw(self, surface):
        """Vẽ button"""
        current_color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2)
        
        # Vẽ text - đảm bảo Unicode
        text_to_render = self.text
        if isinstance(text_to_render, bytes):
            text_to_render = text_to_render.decode('utf-8')
        else:
            text_to_render = str(text_to_render)
        
        text_surface = self.font.render(text_to_render, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def set_text(self, text):
        """Đặt text cho button"""
        self.text = text
    
    def is_clicked(self):
        """Kiểm tra xem button có được click không"""
        return self.is_pressed and self.is_hovered


class IconButton:
    """Nút bấm có icon"""
    
    def __init__(self, x, y, size, image=None, bg_color=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = image
        self.bg_color = bg_color or COLOR_GRAY
        self.is_hovered = False
        self.size = size
    
    def handle_event(self, event):
        """Xử lý sự kiện"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        
        return False
    
    def draw(self, surface):
        """Vẽ icon button"""
        color = (180, 180, 180) if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2)
        
        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)