# 🔮 BOT TỬ VI ĐẠI KỴ — Telegram Bot

Bot Telegram phân tích **Tứ Trụ**, **Ngày Đại Kỵ**, **Vượng/Suy theo Tiết Khí**.

---

## 📁 Cấu trúc

```
daiky_bot/
├── bot.py                  # Entry point chính
├── requirements.txt
├── data/
│   └── profiles.json       # Lưu profile người dùng (tự tạo)
└── core/
    ├── tutu.py             # Tính Tứ Trụ (Năm/Tháng/Ngày/Giờ)
    ├── tietki.py           # 24 Tiết Khí + Vượng/Suy
    ├── daiky.py            # Engine Đại Kỵ + Đồng Pha 4 Khung
    ├── profile.py          # Lưu/đọc profile JSON
    └── caodao.py           # Kho câu ca dao
```

---

## 🚀 Cài đặt & Chạy

### 1. Cài thư viện
```bash
pip install -r requirements.txt
```

### 2. Lấy Bot Token
- Nhắn tin @BotFather trên Telegram
- Dùng lệnh `/newbot` → lấy token

### 3. Cấu hình Token
**Cách A — Biến môi trường (khuyên dùng):**
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
python bot.py
```

**Cách B — Sửa trực tiếp trong bot.py:**
```python
token = "your_token_here"  # dòng cuối file
```

### 4. Deploy lên server (Linux VPS)
```bash
# Chạy nền với screen
screen -S daiky_bot
python bot.py

# Hoặc dùng systemd service
sudo nano /etc/systemd/system/daiky_bot.service
```

```ini
[Unit]
Description=Daiky Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/daiky_bot
Environment=TELEGRAM_BOT_TOKEN=your_token
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable daiky_bot
sudo systemctl start daiky_bot
```

---

## 📋 Lệnh Bot

| Lệnh | Mô tả |
|------|-------|
| `/start` | Chào hỏi + menu lệnh |
| `/setinfo` | Nhập ngày/giờ sinh & giới tính |
| `/tutu` | Xem Tứ Trụ đầy đủ |
| `/vuongsuy` | Phân tích Vượng/Suy 12 tháng tới |
| `/ngaydaiky` | Xem ngày đại kỵ theo tháng/năm |
| `/thangdaiky [T] [Y]` | Xem 1 tháng cụ thể |
| `/homnay` | Phân tích đại kỵ hôm nay |
| `/canhbao [n]` | Cảnh báo trước n ngày (mặc định 30) |
| `/dongpha` | Tìm ngày Đồng Pha 4 Khung |
| `/help` | Hướng dẫn chi tiết |

---

## ⚡ Logic Đại Kỵ

### Mức độ
| Level | Ký hiệu | Tiêu chí |
|-------|---------|---------|
| 0 | ✅ An toàn | Không có xung khắc |
| 1 | 🟢 Nhẹ | Tổng score ≥ 2 |
| 2 | 🟡 Trung | Tổng score ≥ 5 |
| 3 | 🟠 Nặng | Tổng score ≥ 9 |
| 4 | 🔴 Cực kỵ | Đồng Pha 4 Khung |

### Đồng Pha 4 Khung
Xảy ra khi ngày hiện tại có **xung hoặc khắc với CẢ 4 trụ** (Năm + Tháng + Ngày + Giờ).
Đây là ngày kỵ nặng nhất, tuyệt đối tránh làm việc hệ trọng.

### Điểm xung khắc (mỗi cặp trụ)
- Chi xung: +3 điểm
- Can xung: +2 điểm  
- Ngũ hành khắc: +2 điểm
- Hình: +1 điểm

### Lọc tháng kỵ
Nếu **tháng** có trụ tháng xung khắc với Tứ Trụ, các ngày kỵ trong tháng đó sẽ **cộng thêm 1 bậc**.

### Tiết Khí & Vượng/Suy
Nhật Chủ (Can ngày sinh) có 5 trạng thái trong tiết khí:
- 🔥 **Vượng** (10đ) — mạnh nhất
- ⚡ **Tướng** (7đ) — khá mạnh
- 💤 **Hưu** (4đ) — trung bình
- 🔒 **Tù** (2đ) — yếu
- ❄️ **Tử** (0đ) — yếu nhất, cộng thêm 1 bậc kỵ nếu level ≥ 2

---

## 📌 Nhập thông tin

Định dạng: `DD-MM-YYYY-HH:MM-gioi_tinh`
- `15-08-1990-14:30-nam`
- `03-03-1985-06:00-nu`

Giờ sinh ảnh hưởng Trụ Giờ — quan trọng cho phân tích toàn diện!

---

*Built with ❤️ — Tứ Trụ Học Việt Nam*
