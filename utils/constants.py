# Kích thước màn hình
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Bàn cờ Connect Four
ROWS = 6
COLS = 7
CELL_SIZE = 80

# Độ rộng, cao của bàn cờ
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE

# Vị trí bàn cờ trên màn hình (canh giữa)
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2 + 50

# Màu sắc - Tông màu tím-hồng-xanh (Modern Design)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (200, 200, 200)
COLOR_LIGHT_GRAY = (240, 240, 240)
COLOR_DARK_GRAY = (100, 100, 100)

# Tông chính: Tím gradient
COLOR_PURPLE_DARK = (100, 50, 150)      # Tím đậm (dưới)
COLOR_PURPLE_LIGHT = (150, 80, 200)     # Tím nhạt (giữa)
COLOR_PURPLE_BG = (130, 60, 180)        # Tím nền chính

# Màu thẻ chế độ chơi
COLOR_PINK = (255, 100, 150)            # Hồng - Player vs Player
COLOR_BLUE_GAME = (100, 150, 220)       # Xanh dương - Player vs Computer
COLOR_LIGHT_BLUE = (150, 180, 255)      # Xanh nhạt

# Màu nút
COLOR_YELLOW = (255, 200, 50)           # Vàng cho START
COLOR_BUTTON_HOVER = (200, 160, 30)     # Vàng sẫm khi hover
COLOR_EXIT = (220, 80, 80)              # Đỏ cho EXIT

# Màu bàn cờ
COLOR_BOARD_BG = (80, 30, 120)          # Tím sẫm cho nền bàn cờ
COLOR_BOARD_BORDER = (200, 100, 200)    # Tím nhạt cho border

# Màu quân cờ mặc định
COLOR_RED = (255, 100, 120)             # Đỏ nhạt cho quân
COLOR_YELLOW_PIECE = (255, 200, 50)     # Vàng cho quân
COLOR_GREEN = (100, 200, 100)           # Xanh lá

# Default player colors
DEFAULT_P1_COLOR = COLOR_YELLOW
DEFAULT_P2_COLOR = COLOR_RED

# Màn hình
SCREEN_MAIN_MENU = "main_menu"
SCREEN_SETTINGS = "settings"
SCREEN_GAME = "game"
SCREEN_RESULT = "result"

# Font
DEFAULT_FONT_SIZE = 32
LARGE_FONT_SIZE = 48
SMALL_FONT_SIZE = 20

# Trò chơi
GAME_MODE_PVP = "pvp"  # Player vs Player
GAME_MODE_PVC = "pvc"  # Player vs Computer

# Trạng thái game
GAME_STATE_PLAYING = "playing"
GAME_STATE_PAUSED = "paused"
GAME_STATE_FINISHED = "finished"

# Ngôn ngữ
LANG_VN = "vn"
LANG_EN = "en"

# Màu mặc định
DEFAULT_LANGUAGE = LANG_VN
DEFAULT_SOUND_VOLUME = 0.7

# Thời gian animation (ms)
PIECE_FALL_SPEED = 10
PIECE_FALL_DELAY = 50
