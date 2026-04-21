import pygame
from utils.constants import ROWS, COLS, CELL_SIZE, BOARD_X, BOARD_Y
from utils.constants import COLOR_BLACK, COLOR_WHITE

class BoardView:
    """Hiển thị bàn cờ"""
    
    def __init__(self, board_x=BOARD_X, board_y=BOARD_Y, cell_size=CELL_SIZE):
        self.board_x = board_x
        self.board_y = board_y
        self.cell_size = cell_size
        self.board_width = COLS * cell_size
        self.board_height = ROWS * cell_size
        self.board_rect = pygame.Rect(board_x, board_y, self.board_width, self.board_height)
    
    def get_column_from_mouse(self, mouse_x):
        """Lấy cột từ vị trí chuột"""
        if not self.board_rect.collidepoint(mouse_x, self.board_y):
            return -1
        
        relative_x = mouse_x - self.board_x
        col = relative_x // self.cell_size
        
        if 0 <= col < COLS:
            return col
        return -1
    
    def draw(self, surface, board, p1_color, p2_color):
        """
        Vẽ bàn cờ
        Args:
            surface: pygame surface
            board: 2D list từ game_logic
            p1_color: màu quân player 1
            p2_color: màu quân player 2
        """
        from utils.constants import COLOR_BOARD_BG, COLOR_BOARD_BORDER
        
        # Vẽ nền bàn cờ với bo tròn
        pygame.draw.rect(surface, COLOR_BOARD_BG, self.board_rect, border_radius=15)
        pygame.draw.rect(surface, COLOR_BOARD_BORDER, self.board_rect, 4, border_radius=15)
        
        # Vẽ lưới
        for row in range(ROWS):
            for col in range(COLS):
                x = self.board_x + col * self.cell_size
                y = self.board_y + row * self.cell_size
                
                # Vẽ ô
                cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(surface, (80, 80, 120), cell_rect, 1)
                
                # Vẽ nền ô (xanh nhạt)
                pygame.draw.circle(surface, (100, 100, 150), 
                                 (x + self.cell_size // 2, y + self.cell_size // 2),
                                 self.cell_size // 2 - 5)
                
                # Vẽ quân nếu có
                piece = board[row][col]
                if piece != 0:
                    piece_color = p1_color if piece == 1 else p2_color
                    self._draw_piece(surface, x + self.cell_size // 2, 
                                   y + self.cell_size // 2, piece_color)
    
    def _draw_piece(self, surface, cx, cy, color):
        """Vẽ một quân cờ"""
        radius = self.cell_size // 2 - 5
        pygame.draw.circle(surface, color, (cx, cy), radius)
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy), radius, 2)
    
    def get_board_rect(self):
        """Lấy rect của bàn cờ"""
        return self.board_rect
