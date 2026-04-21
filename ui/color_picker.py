import pygame
from utils.constants import COLOR_WHITE, COLOR_BLACK

class ColorPicker:
    """Bộ chọn màu"""
    
    # Các màu có sẵn - Tông màu tím-hồng-xanh modern
    PRESET_COLORS = [
        (255, 200, 50),      # Vàng
        (255, 100, 150),     # Hồng
        (100, 200, 255),     # Xanh dương nhạt
        (255, 150, 80),      # Cam
        (200, 100, 255),     # Tím nhạt
        (80, 200, 200),      # Cyan
        (255, 100, 100),     # Đỏ
        (100, 255, 150),     # Xanh lá
    ]
    
    def __init__(self, x, y, size=50, selected_color=None):
        self.x = x
        self.y = y
        self.size = size
        self.selected_color = selected_color or self.PRESET_COLORS[0]
        self.color_boxes = []
        self._create_color_boxes()
    
    def _create_color_boxes(self):
        """Tạo các ô màu"""
        self.color_boxes = []
        box_x = self.x
        box_y = self.y
        
        for i, color in enumerate(self.PRESET_COLORS):
            if i % 4 == 0 and i > 0:
                box_x = self.x
                box_y += self.size + 5
            
            rect = pygame.Rect(box_x, box_y, self.size, self.size)
            self.color_boxes.append((rect, color))
            box_x += self.size + 5
    
    def handle_event(self, event):
        """Xử lý sự kiện"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, color in self.color_boxes:
                if rect.collidepoint(event.pos):
                    self.selected_color = color
                    return True
        
        return False
    
    def get_selected_color(self):
        """Lấy màu đã chọn"""
        return self.selected_color
    
    def set_selected_color(self, color):
        """Đặt màu đã chọn"""
        self.selected_color = color
    
    def draw(self, surface):
        """Vẽ các ô màu"""
        for rect, color in self.color_boxes:
            pygame.draw.rect(surface, color, rect)
            
            # Vẽ border đặc biệt nếu là màu được chọn
            if color == self.selected_color:
                pygame.draw.rect(surface, COLOR_BLACK, rect, 4)
            else:
                pygame.draw.rect(surface, COLOR_BLACK, rect, 1)