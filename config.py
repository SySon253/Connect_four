# ============================================================================
# CONFIG.PY - Cấu hình ứng dụng
# ============================================================================

import pygame

# Khởi tạo pygame
pygame.init()

# Screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Màu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Khỏi tạo display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect Four")
clock = pygame.time.Clock()
