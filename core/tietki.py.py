"""
core/tietki.py — 24 Tiết Khí & Phân tích Vượng/Suy theo Ngũ Hành
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import math


# ── 24 Tiết Khí (dương lịch gần đúng, sai số ≤ 1-2 ngày) ────────────────────
# Format: (tháng, ngày, tên tiết, tháng âm lịch tương ứng)
TIET_KHI_BASE = [
    # (month, day_approx, name, lunar_month, ngu_hanh_season)
    (1,  6,  "Tiểu Hàn",    11, "Thủy"),
    (1,  20, "Đại Hàn",     12, "Thủy"),
    (2,  4,  "Lập Xuân",     1, "Mộc"),
    (2,  19, "Vũ Thủy",      1, "Mộc"),
    (3,  6,  "Kinh Trập",    2, "Mộc"),
    (3,  21, "Xuân Phân",    2, "Mộc"),
    (4,  5,  "Thanh Minh",   3, "Mộc"),
    (4,  20, "Cốc Vũ",       3, "Mộc"),
    (5,  6,  "Lập Hạ",       4, "Hỏa"),
    (5,  21, "Tiểu Mãn",     4, "Hỏa"),
    (6,  6,  "Mang Chủng",   5, "Hỏa"),
    (6,  21, "Hạ Chí",       5, "Hỏa"),
    (7,  7,  "Tiểu Thử",     6, "Hỏa"),
    (7,  23, "Đại Thử",      6, "Hỏa"),
    (8,  7,  "Lập Thu",      7, "Kim"),
    (8,  23, "Xử Thử",       7, "Kim"),
    (9,  8,  "Bạch Lộ",      8, "Kim"),
    (9,  23, "Thu Phân",     8, "Kim"),
    (10, 8,  "Hàn Lộ",       9, "Kim"),
    (10, 23, "Sương Giáng",   9, "Kim"),
    (11, 7,  "Lập Đông",     10, "Thủy"),
    (11, 22, "Tiểu Tuyết",   10, "Thủy"),
    (12, 7,  "Đại Tuyết",    11, "Thủy"),
    (12, 22, "Đông Chí",     11, "Thủy"),
]

# ── Trạng thái Vượng/Suy của từng Ngũ Hành theo mùa/tiết ────────────────────
# Theo lý thuyết Tứ Trụ: Vượng=10, Tướng=7, Hưu=4, Tù=2, Tử=0
#
# Mùa Xuân (Lập Xuân → Lập Hạ): Mộc Vượng
# Mùa Hạ  (Lập Hạ → Lập Thu):  Hỏa Vượng
# Mùa Thu  (Lập Thu → Lập Đông): Kim Vượng
# Mùa Đông (Lập Đông → Lập Xuân): Thủy Vượng
# Giao thời (Thổ): Thổ Vượng ở 4 giao mùa (Thìn, Mùi, Tuất, Sửu tháng)
#
# Bảng đầy đủ 5 hành × 4 mùa:
VUONG_SUY_TABLE = {
    # Tiết → {hanh: (trang_thai, diem)}
    "Lập Xuân": {"Mộc": ("Vượng", 10), "Hỏa": ("Tướng", 7), "Thổ": ("Tử", 0), "Kim": ("Tù", 2), "Thủy": ("Hưu", 4)},
    "Vũ Thủy":  {"Mộc": ("Vượng", 10), "Hỏa": ("Tướng", 7), "Thổ": ("Tử", 0), "Kim": ("Tù", 2), "Thủy": ("Hưu", 4)},
    "Kinh Trập":{"Mộc": ("Vượng", 10), "Hỏa": ("Tướng", 7), "Thổ": ("Tử", 0), "Kim": ("Tù", 2), "Thủy": ("Hưu", 4)},
    "Xuân Phân":{"Mộc": ("Vượng", 10), "Hỏa": ("Tướng", 7), "Thổ": ("Tử", 0), "Kim": ("Tù", 2), "Thủy": ("Hưu", 4)},
    "Thanh Minh":{"Mộc": ("Vượng", 10), "Hỏa": ("Tướng", 7), "Thổ": ("Hưu", 4), "Kim": ("Tù", 2), "Thủy": ("Tử", 0)},
    "Cốc Vũ":   {"Mộc": ("Vượng", 10), "Hỏa": ("Tướng", 7), "Thổ": ("Hưu", 4), "Kim": ("Tù", 2), "Thủy": ("Tử", 0)},
    "Lập Hạ":   {"Hỏa": ("Vượng", 10), "Thổ": ("Tướng", 7), "Mộc": ("Hưu", 4), "Thủy": ("Tù", 2), "Kim": ("Tử", 0)},
    "Tiểu Mãn": {"Hỏa": ("Vượng", 10), "Thổ": ("Tướng", 7), "Mộc": ("Hưu", 4), "Thủy": ("Tù", 2), "Kim": ("Tử", 0)},
    "Mang Chủng":{"Hỏa": ("Vượng", 10), "Thổ": ("Tướng", 7), "Mộc": ("Hưu", 4), "Thủy": ("Tù", 2), "Kim": ("Tử", 0)},
    "Hạ Chí":   {"Hỏa": ("Vượng", 10), "Thổ": ("Tướng", 7), "Mộc": ("Hưu", 4), "Thủy": ("Tù", 2), "Kim": ("Tử", 0)},
    "Tiểu Thử": {"Hỏa": ("Vượng", 10), "Thổ": ("Tướng", 7), "Mộc": ("Hưu", 4), "Thủy": ("Tù", 2), "Kim": ("Tử", 0)},
    "Đại Thử":  {"Hỏa": ("Vượng", 10), "Thổ": ("Tướng", 7), "Mộc": ("Hưu", 4), "Thủy": ("Tù", 2), "Kim": ("Tử", 0)},
    "Lập Thu":  {"Kim": ("Vượng", 10), "Thủy": ("Tướng", 7), "Thổ": ("Hưu", 4), "Hỏa": ("Tù", 2), "Mộc": ("Tử", 0)},
    "Xử Thử":   {"Kim": ("Vượng", 10), "Thủy": ("Tướng", 7), "Thổ": ("Hưu", 4), "Hỏa": ("Tù", 2), "Mộc": ("Tử", 0)},
    "Bạch Lộ":  {"Kim": ("Vượng", 10), "Thủy": ("Tướng", 7), "Thổ": ("Hưu", 4), "Hỏa": ("Tù", 2), "Mộc": ("Tử", 0)},
    "Thu Phân":  {"Kim": ("Vượng", 10), "Thủy": ("Tướng", 7), "Thổ": ("Hưu", 4), "Hỏa": ("Tù", 2), "Mộc": ("Tử", 0)},
    "Hàn Lộ":   {"Kim": ("Vượng", 10), "Thủy": ("Tướng", 7), "Thổ": ("Hưu", 4), "Hỏa": ("Tù", 2), "Mộc": ("Tử", 0)},
    "Sương Giáng":{"Kim": ("Vượng", 10), "Thủy": ("Tướng", 7), "Thổ": ("Hưu", 4), "Hỏa": ("Tù", 2), "Mộc": ("Tử", 0)},
    "Lập Đông":  {"Thủy": ("Vượng", 10), "Mộc": ("Tướng", 7), "Kim": ("Hưu", 4), "Thổ": ("Tù", 2), "Hỏa": ("Tử", 0)},
    "Tiểu Tuyết":{"Thủy": ("Vượng", 10), "Mộc": ("Tướng", 7), "Kim": ("Hưu", 4), "Thổ": ("Tù", 2), "Hỏa": ("Tử", 0)},
    "Đại Tuyết": {"Thủy": ("Vượng", 10), "Mộc": ("Tướng", 7), "Kim": ("Hưu", 4), "Thổ": ("Tù", 2), "Hỏa": ("Tử", 0)},
    "Đông Chí":  {"Thủy": ("Vượng", 10), "Mộc": ("Tướng", 7), "Kim": ("Hưu", 4), "Thổ": ("Tù", 2), "Hỏa": ("Tử", 0)},
    "Tiểu Hàn":  {"Thủy": ("Vượng", 10), "Mộc": ("Tướng", 7), "Kim": ("Hưu", 4), "Thổ": ("Tù", 2), "Hỏa": ("Tử", 0)},
    "Đại Hàn":   {"Thủy": ("Vượng", 10), "Mộc": ("Tướng", 7), "Kim": ("Hưu", 4), "Thổ": ("Tù", 2), "Hỏa": ("Tử", 0)},
}


class TietKiEngine:
    def __init__(self):
        pass

    def _get_tietki_dates(self, year: int):
        """Trả về danh sách Tiết Khí với ngày bắt đầu/kết thúc cho một năm."""
        entries = []
        for (month, day, name, lunar_month, season_hanh) in TIET_KHI_BASE:
            try:
                start = datetime(year, month, day)
            except ValueError:
                start = datetime(year, month, min(day, 28))
            entries.append({
                "name": name,
                "start_date": start,
                "lunar_month": lunar_month,
                "season_hanh": season_hanh,
            })

        # Thêm năm kế (lấy tiết khí đầu năm sau)
        for (month, day, name, lunar_month, season_hanh) in TIET_KHI_BASE[:4]:
            try:
                start = datetime(year + 1, month, day)
            except ValueError:
                start = datetime(year + 1, month, min(day, 28))
            entries.append({
                "name": name,
                "start_date": start,
                "lunar_month": lunar_month,
                "season_hanh": season_hanh,
            })

        # Sort by date
        entries.sort(key=lambda x: x["start_date"])

        # Gán end_date = start của tiết tiếp theo - 1 ngày
        for i in range(len(entries) - 1):
            entries[i]["end_date"] = entries[i + 1]["start_date"] - timedelta(days=1)
        entries[-1]["end_date"] = entries[-1]["start_date"] + timedelta(days=15)

        return entries

    def get_current_tietki(self, dt: datetime) -> Dict:
        """Lấy Tiết Khí hiện tại tại ngày dt."""
        year = dt.year
        entries = self._get_tietki_dates(year - 1) + self._get_tietki_dates(year)

        for entry in reversed(entries):
            if dt >= entry["start_date"]:
                return entry

        # Fallback
        return {
            "name": "Tiểu Hàn",
            "start_date": datetime(year, 1, 6),
            "end_date": datetime(year, 1, 19),
            "lunar_month": 11,
            "season_hanh": "Thủy"
        }

    def get_tietki_of_month(self, month: int, year: int) -> str:
        """Lấy tên Tiết Khí chính của tháng dương lịch."""
        dt = datetime(year, month, 15)
        tk = self.get_current_tietki(dt)
        return tk["name"]

    def analyze_vuong_suy(self, ngu_hanh: str, tietki_name: str) -> Dict:
        """
        Phân tích trạng thái Vượng/Suy của một Ngũ Hành trong tiết khí.
        """
        table = VUONG_SUY_TABLE.get(tietki_name, {})
        if ngu_hanh in table:
            trang_thai, diem = table[ngu_hanh]
        else:
            trang_thai, diem = "Hưu", 4

        return {
            "ngu_hanh": ngu_hanh,
            "tietki": tietki_name,
            "trang_thai": trang_thai,
            "diem": diem,
        }

    def get_season_strength(self, dt: datetime, ngu_hanh: str) -> int:
        """Trả về điểm Vượng/Suy (0-10) tại ngày dt."""
        tk = self.get_current_tietki(dt)
        vs = self.analyze_vuong_suy(ngu_hanh, tk["name"])
        return vs["diem"]
