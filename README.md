# Connect Four Game - Python Pygame

Một trò chơi Connect Four hoàn chỉnh được phát triển bằng Python và Pygame, hỗ trợ chơi 1vs1 và vs AI với giao diện desktop hiện đại.

## Tính năng

- **2 chế độ chơi**: Người vs Người (PVP) hoặc Người vs Máy (PVC)
- **AI thông minh**: Sử dụng thuật toán Minimax với Alpha-Beta Pruning
- **Hỗ trợ 2 ngôn ngữ**: Tiếng Việt và Tiếng Anh
- **Tùy chỉnh**: Chọn màu quân cờ, điều chỉnh âm lượng
- **Timer**: Bộ đếm thời gian cho mỗi trận đấu
- **Giao diện thân thiện**: UI hiện đại, dễ sử dụng
- **Lưu cài đặt**: Tất cả cài đặt được lưu vào file JSON

## Yêu cầu

- Python 3.7+
- pygame

## Cài đặt

### 1. Clone hoặc download project

```bash
cd connect-four
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Hoặc nếu bạn dùng `pip3`:

```bash
pip3 install -r requirements.txt
```

## Chạy game

```bash
python main.py
```

Hoặc:

```bash
python3 main.py
```

## Cấu trúc project

```
connect_four/
├── main.py                      # Entry point
├── config.py                    # Cấu hình pygame
├── requirements.txt             # Dependencies
├── README.md                    # Hướng dẫn
├── settings.json               # File lưu cài đặt (tự động tạo)
│
├── assets/
│   ├── images/                 # Thư mục hình ảnh
│   ├── fonts/                  # Thư mục font chữ
│   └── sounds/                 # Thư mục âm thanh
│
├── core/
│   ├── game_logic.py           # Logic chơi game (6x7 board)
│   ├── ai_player.py            # AI đối thủ (Minimax)
│   ├── timer_manager.py        # Quản lý bộ đếm thời gian
│   └── state_manager.py        # Quản lý trạng thái app
│
├── ui/
│   ├── button.py               # Component button
│   ├── label.py                # Component label/text
│   ├── slider.py               # Component slider
│   ├── color_picker.py         # Component chọn màu
│   ├── panel.py                # Component panel
│   └── board_view.py           # Hiển thị bàn cờ
│
├── screens/
│   ├── main_menu.py            # Màn hình menu chính
│   ├── settings_screen.py      # Màn hình cài đặt
│   ├── game_screen.py          # Màn hình chơi game
│   └── result_screen.py        # Màn hình kết quả
│
└── utils/
    ├── constants.py            # Hằng số chung
    ├── helpers.py              # Hàm helper
    └── asset_loader.py         # Tải assets
```

## Hướng dẫn chơi

### Menu chính
- Chọn chế độ chơi: **NGƯỜI VS NGƯỜI** hoặc **NGƯỜI VS MÁY**
- Nhấn **START** để bắt đầu
- Nhấn **EXIT** để thoát
- Nhấn icon **bánh răng** để vào Settings

### Cài đặt (Settings)
- **Ngôn ngữ**: Chọn VN (Tiếng Việt) hoặc EN (Tiếng Anh)
- **Âm thanh**: Điều chỉnh âm lượng bằng slider
- **Màu Quân 1**: Chọn màu cho quân cờ của người chơi 1
- **Màu Quân 2**: Chọn màu cho quân cờ của người chơi 2
- **LƯU**: Lưu cài đặt
- **QUAY LẠI**: Quay lại menu chính

### Chơi game
- **Click cột**: Click trên cột để thả quân
- **Player Turn**: Hiển thị lượt chơi hiện tại (Quân 1 / Quân 2 / AI)
- **Timer**: Bộ đếm thời gian trận đấu
- **Icon Settings**: Tạm dừng game và vào settings
- **Icon Restart**: Chơi lại trận hiện tại
- **Icon Exit**: Thoát về menu chính

### Kết quả
- Màn hình hiển thị người thắng / hòa
- **TRANG CHỦ**: Quay lại menu chính
- **CHƠI LẠI**: Bắt đầu trò chơi mới

## Luật chơi Connect Four

- Bàn cờ: **6 hàng × 7 cột**
- Mục tiêu: Tạo một hàng **4 quân liên tiếp**
- Hướng: Ngang, dọc, chéo lên, chéo xuống
- Quân rơi: Quân rơi xuống vị trí trống thấp nhất trong cột
- Thắng: Ai có 4 quân liên tiếp trước tiên
- Hòa: Khi bàn cờ đầy mà không ai thắng

## AI

Game có 2 mức AI:
- **Mức vừa (Default)**: Sử dụng heuristic - AI sẽ ưu tiên:
  - Thắng ngay nếu có cơ hội
  - Chặn đối thủ nếu sắp thắng
  - Chọn vị trí tốt nhất dựa trên điểm số
- **Mức khó**: Sử dụng Minimax + Alpha-Beta Pruning (có thể thêm vào sau)

## Tệp cài đặt

Cài đặt được lưu trong file `settings.json`:

```json
{
  "language": "vn",
  "sound_volume": 0.7,
  "player1_color": [255, 193, 7],
  "player2_color": [220, 53, 69]
}
```

## Troubleshooting

### Lỗi: "No module named 'pygame'"
Giải pháp: Cài đặt pygame
```bash
pip install pygame
```

### Lỗi: Cửa sổ không hiển thị
- Kiểm tra version pygame
- Thử cập nhật pygame: `pip install --upgrade pygame`

### Lỗi: AI chơi quá chậm
- Giảm độ sâu của Minimax trong `ai_player.py` (thay đổi `depth=4` thành `depth=3`)

## Phát triển trong tương lai

- [ ] Thêm mức AI khó hơn (Minimax đầy đủ)
- [ ] Thêm âm thanh (click, win, lose)
- [ ] Thêm animation quân rơi
- [ ] Thêm chế độ online multiplayer
- [ ] Thêm highlight 4 quân thắng
- [ ] Lịch sử đấu
- [ ] Leaderboard

## Tác giả

Phát triển bằng Python 3 + Pygame

## License

MIT
