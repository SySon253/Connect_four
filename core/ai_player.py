# ============================================================================
# AI_PLAYER.PY - AI đối thủ máy
# ============================================================================

import random
from utils.constants import ROWS, COLS

class AIPlayer:
    """AI player cho chế độ vs Computer"""
    
    def __init__(self, difficulty=1):
        """
        Khởi tạo AI
        difficulty: 0 = dễ (random), 1 = vừa (heuristic), 2 = khó (minimax)
        """
        self.difficulty = difficulty
        self.ai_player = 2  # AI luôn là player 2
    
    def get_move(self, board):
        """
        Lấy nước đi của AI
        Args: board = 2D list biểu diễn bàn cờ
        Returns: cột (0-6)
        """
        if self.difficulty == 0:
            return self._get_random_move(board)
        elif self.difficulty == 1:
            return self._get_heuristic_move(board)
        else:
            return self._get_minimax_move(board, depth=4)
    
    def _get_random_move(self, board):
        """Nước đi ngẫu nhiên"""
        valid_moves = [col for col in range(COLS) if board[0][col] == 0]
        return random.choice(valid_moves) if valid_moves else 0
    
    def _get_heuristic_move(self, board):
        """Nước đi dùng heuristic"""
        valid_moves = [col for col in range(COLS) if board[0][col] == 0]
        
        if not valid_moves:
            return 0
        
        # Ưu tiên 1: Nước thắng
        for col in valid_moves:
            if self._is_winning_move(board, col, self.ai_player):
                return col
        
        # Ưu tiên 2: Chặn nước thắng của đối thủ
        for col in valid_moves:
            if self._is_winning_move(board, col, 1):  # 1 = human player
                return col
        
        # Ưu tiên 3: Nước tốt nhất theo điểm
        scores = [(col, self._evaluate_position(board, col)) for col in valid_moves]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[0][0] if scores else random.choice(valid_moves)
    
    def _get_minimax_move(self, board, depth=4):
        """Nước đi dùng minimax với alpha-beta pruning"""
        valid_moves = [col for col in range(COLS) if board[0][col] == 0]
        
        if not valid_moves:
            return 0
        
        best_score = float('-inf')
        best_move = valid_moves[0]
        
        for col in valid_moves:
            score = self._minimax(board, depth - 1, float('-inf'), float('inf'), False, col)
            if score > best_score:
                best_score = score
                best_move = col
        
        return best_move
    
    def _minimax(self, board, depth, alpha, beta, is_maximizing, last_col=None):
        """Minimax với alpha-beta pruning"""
        # Kiểm tra thắng
        if last_col is not None:
            row = self._find_row_for_col(board, last_col)
            if row >= 0:
                player = board[row][last_col]
                if self._is_winning_at(board, row, last_col):
                    return 100 if player == self.ai_player else -100
        
        # Kiểm tra draw
        if all(board[0][col] != 0 for col in range(COLS)):
            return 0
        
        # Dừng tìm kiếm
        if depth == 0:
            return self._evaluate_board(board)
        
        valid_moves = [col for col in range(COLS) if board[0][col] == 0]
        
        if is_maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                board_copy = [row[:] for row in board]
                row = self._place_piece(board_copy, col, self.ai_player)
                eval = self._minimax(board_copy, depth - 1, alpha, beta, False, col)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                board_copy = [row[:] for row in board]
                row = self._place_piece(board_copy, col, 1)
                eval = self._minimax(board_copy, depth - 1, alpha, beta, True, col)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def _place_piece(self, board, col, player):
        """Thả quân vào cột và trả về hàng"""
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == 0:
                board[row][col] = player
                return row
        return -1
    
    def _find_row_for_col(self, board, col):
        """Tìm hàng nơi quân sẽ được thả"""
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == 0:
                return row
        return -1
    
    def _is_winning_move(self, board, col, player):
        """Kiểm tra xem nước này có thắng không"""
        board_copy = [row[:] for row in board]
        row = self._place_piece(board_copy, col, player)
        return self._is_winning_at(board_copy, row, col)
    
    def _is_winning_at(self, board, row, col):
        """Kiểm tra xem có 4 quân liên tiếp tại (row, col)"""
        if row < 0:
            return False
        
        player = board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1
            x, y = row + dx, col + dy
            while 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == player:
                count += 1
                x += dx
                y += dy
            
            x, y = row - dx, col - dy
            while 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == player:
                count += 1
                x -= dx
                y -= dy
            
            if count >= 4:
                return True
        
        return False
    
    def _evaluate_position(self, board, col):
        """Đánh giá điểm của một vị trí"""
        score = 0
        
        # Thích cột giữa
        center_col = COLS // 2
        score += abs(col - center_col) * (-5)
        
        # Đánh giá các pattern
        board_copy = [row[:] for row in board]
        row = self._place_piece(board_copy, col, self.ai_player)
        
        if row >= 0:
            score += self._count_patterns(board_copy, row, col, self.ai_player) * 10
            score -= self._count_patterns(board_copy, row, col, 1) * 8
        
        return score
    
    def _count_patterns(self, board, row, col, player):
        """Đếm các pattern tốt của người chơi tại vị trí"""
        patterns = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            for _ in range(3):
                x, y = row + dx, col + dy
                count = 0
                while 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == player:
                    count += 1
                    x += dx
                    y += dy
                patterns += max(0, count - 2)
        
        return patterns
    
    def _evaluate_board(self, board):
        """Đánh giá toàn bộ bàn cờ"""
        score = 0
        
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] != 0:
                    player = board[row][col]
                    value = 1 if player == self.ai_player else -1
                    score += value * self._count_patterns(board, row, col, player)
        
        return score
