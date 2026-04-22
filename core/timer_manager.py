# ============================================================================
# TIMER_MANAGER.PY - Quản lý bộ đếm thời gian
# ============================================================================

import pygame

class TimerManager:
    """Quản lý timer cho trò chơi"""
    
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0  # milliseconds
        self.is_running = False
        self.paused_time = 0
        # Đảm bảo pygame được init
        if not pygame.get_init():
            pygame.init()
    
    def start(self):
        """Bắt đầu timer"""
        self.start_time = pygame.time.get_ticks()
        self.is_running = True
        self.elapsed_time = 0
        self.paused_time = 0
    
    def pause(self):
        """Tạm dừng timer"""
        if self.is_running:
            self.paused_time = pygame.time.get_ticks()
            self.is_running = False
    
    def resume(self):
        """Tiếp tục timer"""
        if not self.is_running and self.start_time is not None:
            elapsed_during_pause = pygame.time.get_ticks() - self.paused_time
            self.start_time += elapsed_during_pause
            self.is_running = True
    
    def reset(self):
        """Reset timer"""
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.paused_time = 0
    
    def get_elapsed_time(self):
        """Lấy thời gian đã trôi qua (milliseconds)"""
        if self.start_time is None:
            return 0
        
        if self.is_running:
            return pygame.time.get_ticks() - self.start_time
        else:
            return self.paused_time - self.start_time
    
    def get_formatted_time(self):
        """Lấy thời gian dưới dạng MM:SS"""
        elapsed = self.get_elapsed_time()
        total_seconds = elapsed // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def is_timer_running(self):
        """Kiểm tra timer có đang chạy không"""
        return self.is_running
