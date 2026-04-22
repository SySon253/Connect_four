# ============================================================================
# GAME_LOGIC.PY - Logic cốt lõi của trò chơi Connect Four
# ============================================================================

from utils.constants import ROWS, COLS

class ConnectFourGame:
    """Quản lý logic trò chơi Connect Four"""
    
    def __init__(self):
        """Khởi tạo bàn cờ"""
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.move_history = []
    
    def reset(self):
        """Reset bàn cờ"""
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.move_history = []
    
    def is_valid_move(self, col):
        """Kiểm tra cột có hợp lệ không (có chỗ trống)"""
        if col < 0 or col >= COLS:
            return False
        return self.board[0][col] == 0
    
    def make_move(self, col):
        """
        Thực hiện nước đi: thả quân xuống cột
        Returns: row nếu thành công, -1 nếu thất bại
        """
        if not self.is_valid_move(col):
            return -1
        
        # Tìm hàng cuối cùng (từ dưới lên)
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.move_history.append((row, col, self.current_player))
                
                # Kiểm tra thắng
                if self.check_win(row, col):
                    self.game_over = True
                    self.winner = self.current_player
                
                # Kiểm tra hòa
                if self.is_board_full():
                    self.game_over = True
                    self.winner = 0  # 0 = hòa
                
                # Chuyển người chơi
                self.current_player = 3 - self.current_player  # 1->2, 2->1
                return row
        
        return -1
    
    def check_win(self, row, col):
        """Kiểm tra xem nước đi vừa rồi có tạo thắng không"""
        player = self.board[row][col]
        
        # Kiểm tra theo 4 hướng: ngang, dọc, chéo /, chéo \
        directions = [
            (0, 1),   # Ngang
            (1, 0),   # Dọc
            (1, 1),   # Chéo \
            (1, -1)   # Chéo /
        ]
        
        for dx, dy in directions:
            count = 1
            
            # Kiểm tra hướng dương
            x, y = row + dx, col + dy
            while 0 <= x < ROWS and 0 <= y < COLS and self.board[x][y] == player:
                count += 1
                x += dx
                y += dy
            
            # Kiểm tra hướng âm
            x, y = row - dx, col - dy
            while 0 <= x < ROWS and 0 <= y < COLS and self.board[x][y] == player:
                count += 1
                x -= dx
                y -= dy
            
            if count >= 4:
                return True
        
        return False
    
    def is_board_full(self):
        """Kiểm tra bàn cờ có đầy không"""
        return all(self.board[0][col] != 0 for col in range(COLS))
    
    def get_board(self):
        """Lấy trạng thái bàn cờ"""
        return self.board
    
    def get_current_player(self):
        """Lấy người chơi hiện tại"""
        return self.current_player
    
    def is_game_over(self):
        """Kiểm tra game có kết thúc không"""
        return self.game_over
    
    def get_winner(self):
        """
        Lấy thông tin người thắng
        Returns: 1 (P1 thắng), 2 (P2 thắng), 0 (hòa), None (chưa kết thúc)
        """
        return self.winner
    
    def get_valid_moves(self):
        """Lấy danh sách các nước đi hợp lệ"""
        return [col for col in range(COLS) if self.is_valid_move(col)]
    
    def get_piece_at(self, row, col):
        """Lấy quân tại vị trí (row, col)"""
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return 0
    
    def undo_last_move(self):
        """Undo nước đi cuối cùng"""
        if self.move_history:
            row, col, player = self.move_history.pop()
            self.board[row][col] = 0
            self.current_player = player
            self.game_over = False
            self.winner = None
