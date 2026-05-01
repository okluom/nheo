"""
core/tutu.py — Tính Tứ Trụ (Năm, Tháng, Ngày, Giờ)
Thiên Can + Địa Chi + Tàng Can + Ngũ Hành + Vượng Suy
"""

from datetime import datetime
from typing import Dict, Any

# ── Thiên Can ──────────────────────────────────────────────────────────────────
THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

CAN_HANH = {
    "Giáp": "Mộc", "Ất": "Mộc",
    "Bính": "Hỏa", "Đinh": "Hỏa",
    "Mậu": "Thổ", "Kỷ": "Thổ",
    "Canh": "Kim", "Tân": "Kim",
    "Nhâm": "Thủy", "Quý": "Thủy",
}

CAN_AM_DUONG = {
    "Giáp": "Dương", "Ất": "Âm",
    "Bính": "Dương", "Đinh": "Âm",
    "Mậu": "Dương", "Kỷ": "Âm",
    "Canh": "Dương", "Tân": "Âm",
    "Nhâm": "Dương", "Quý": "Âm",
}

# ── Địa Chi ──────────────────────────────────────────────────────────────────
DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

CHI_HANH = {
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
    "Thìn": "Thổ", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy",
}

CHI_AM_DUONG = {
    "Tý": "Dương", "Sửu": "Âm", "Dần": "Dương", "Mão": "Âm",
    "Thìn": "Dương", "Tỵ": "Âm", "Ngọ": "Dương", "Mùi": "Âm",
    "Thân": "Dương", "Dậu": "Âm", "Tuất": "Dương", "Hợi": "Âm",
}

# Tàng Can trong mỗi Địa Chi (can tàng chính + phụ)
TANG_CAN = {
    "Tý":   ["Quý"],
    "Sửu":  ["Kỷ", "Tân", "Quý"],
    "Dần":  ["Giáp", "Bính", "Mậu"],
    "Mão":  ["Ất"],
    "Thìn": ["Mậu", "Ất", "Quý"],
    "Tỵ":   ["Bính", "Mậu", "Canh"],
    "Ngọ":  ["Đinh", "Kỷ"],
    "Mùi":  ["Kỷ", "Đinh", "Ất"],
    "Thân": ["Canh", "Nhâm", "Mậu"],
    "Dậu":  ["Tân"],
    "Tuất": ["Mậu", "Tân", "Đinh"],
    "Hợi":  ["Nhâm", "Giáp"],
}

# ── Lục Thập Hoa Giáp xét Can–Chi ghép ──────────────────────────────────────
# Can & Chi phải cùng Âm-Dương (hoặc cùng chỉ số chẵn/lẻ)

# ── Xung ─────────────────────────────────────────────────────────────────────
# Lục xung Địa Chi
XUNG_CHI = {
    "Tý": "Ngọ", "Ngọ": "Tý",
    "Sửu": "Mùi", "Mùi": "Sửu",
    "Dần": "Thân", "Thân": "Dần",
    "Mão": "Dậu", "Dậu": "Mão",
    "Thìn": "Tuất", "Tuất": "Thìn",
    "Tỵ": "Hợi", "Hợi": "Tỵ",
}

# Thiên Can xung (cách 6 vị)
XUNG_CAN = {
    "Giáp": "Canh", "Canh": "Giáp",
    "Ất": "Tân", "Tân": "Ất",
    "Bính": "Nhâm", "Nhâm": "Bính",
    "Đinh": "Quý", "Quý": "Đinh",
    "Mậu": "Giáp",  # Mậu xung Giáp (khắc)
    "Kỷ": "Ất",
}

# ── Khắc (ngũ hành tương khắc) ───────────────────────────────────────────────
KHAC_HANH = {
    "Mộc": "Thổ",   # Mộc khắc Thổ
    "Thổ": "Thủy",  # Thổ khắc Thủy
    "Thủy": "Hỏa",  # Thủy khắc Hỏa
    "Hỏa": "Kim",   # Hỏa khắc Kim
    "Kim": "Mộc",   # Kim khắc Mộc
}

# Bị khắc bởi:
BI_KHAC_BOI = {v: k for k, v in KHAC_HANH.items()}

# ── Hình, Hại, Phá ───────────────────────────────────────────────────────────
HINH_CHI = {
    "Dần": "Tỵ", "Tỵ": "Thân", "Thân": "Dần",   # Vô ân hình
    "Sửu": "Tuất", "Tuất": "Mùi", "Mùi": "Sửu",  # Thế lực hình
    "Tý": "Mão", "Mão": "Tý",                       # Vô lễ hình
    "Thìn": "Thìn", "Ngọ": "Ngọ",
    "Dậu": "Dậu", "Hợi": "Hợi",                    # Tự hình
}

# ── Lục Hợp ──────────────────────────────────────────────────────────────────
HOP_CHI = {
    "Tý": "Sửu", "Sửu": "Tý",
    "Dần": "Hợi", "Hợi": "Dần",
    "Mão": "Tuất", "Tuất": "Mão",
    "Thìn": "Dậu", "Dậu": "Thìn",
    "Tỵ": "Thân", "Thân": "Tỵ",
    "Ngọ": "Mùi", "Mùi": "Ngọ",
}

# ── Tam Hợp ──────────────────────────────────────────────────────────────────
TAM_HOP = [
    {"Dần", "Ngọ", "Tuất"},  # Hỏa cục
    {"Thân", "Tý", "Thìn"},  # Thủy cục
    {"Tỵ", "Dậu", "Sửu"},   # Kim cục
    {"Hợi", "Mão", "Mùi"},   # Mộc cục
]

# ── Mệnh (theo Can năm) ──────────────────────────────────────────────────────
MENH_MAP = {
    "Giáp": "Mộc", "Ất": "Mộc",
    "Bính": "Hỏa", "Đinh": "Hỏa",
    "Mậu": "Thổ", "Kỷ": "Thổ",
    "Canh": "Kim", "Tân": "Kim",
    "Nhâm": "Thủy", "Quý": "Thủy",
}

# ── Trụ giờ theo giờ thực (Địa Chi giờ) ─────────────────────────────────────
# Mỗi Chi = 2 giờ
HOUR_TO_CHI = {
    23: "Tý", 0: "Tý",
    1: "Sửu", 2: "Sửu",
    3: "Dần", 4: "Dần",
    5: "Mão", 6: "Mão",
    7: "Thìn", 8: "Thìn",
    9: "Tỵ", 10: "Tỵ",
    11: "Ngọ", 12: "Ngọ",
    13: "Mùi", 14: "Mùi",
    15: "Thân", 16: "Thân",
    17: "Dậu", 18: "Dậu",
    19: "Tuất", 20: "Tuất",
    21: "Hợi", 22: "Hợi",
}

# Can giờ theo Can ngày (lấy can từ bảng Ngũ Hổ Độn)
# Can ngày: 0=Giáp/Kỷ, 1=Ất/Canh, 2=Bính/Tân, 3=Đinh/Nhâm, 4=Mậu/Quý
HOUR_CAN_BASE = {
    "Giáp": 0, "Kỷ": 0,
    "Ất": 2, "Canh": 2,
    "Bính": 4, "Tân": 4,
    "Đinh": 6, "Nhâm": 6,
    "Mậu": 8, "Quý": 8,
}


class TuTruCalculator:
    def __init__(self, tietki_engine=None):
        self.tietki_engine = tietki_engine

    def _can_index(self, can: str) -> int:
        return THIEN_CAN.index(can)

    def _chi_index(self, chi: str) -> int:
        return DIA_CHI.index(chi)

    # ── Trụ Năm ──────────────────────────────────────────────────────────────
    def get_year_pillar(self, year: int) -> Dict:
        """
        Năm Giáp Tý = 1984. Tính từ đó.
        Lưu ý: đổi năm âm lịch theo Lập Xuân (khoảng 4/2 dương lịch)
        """
        # Mốc: 1984 = Giáp Tý
        can_idx = (year - 4) % 10
        chi_idx = (year - 4) % 12
        can = THIEN_CAN[can_idx]
        chi = DIA_CHI[chi_idx]
        return self._build_pillar(can, chi)

    # ── Trụ Tháng ────────────────────────────────────────────────────────────
    def get_month_pillar(self, year: int, month: int, day: int) -> Dict:
        """
        Tháng tính theo Tiết (Tiết Khí).
        Tháng Giêng (Dần) = từ Lập Xuân.
        Can tháng theo Ngũ Hổ Độn (dựa vào Can năm).
        """
        # Xác định tháng âm lịch theo tiết
        if self.tietki_engine:
            dt = datetime(year, month, day)
            tk = self.tietki_engine.get_current_tietki(dt)
            lunar_month = tk.get("lunar_month", month)
        else:
            # Approximate: dương tháng → âm tháng lệch ~1
            lunar_month = month - 1 if month > 1 else 12

        # Chi tháng: Dần=1, Mão=2,...
        chi_idx = (lunar_month + 1) % 12  # Tháng 1 = Dần (index 2)
        # Thực ra: tháng âm 1 = Dần (chi idx 2), 2=Mão(3),...12=Sửu(1)
        chi_map = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7,
                   7: 8, 8: 9, 9: 10, 10: 11, 11: 0, 12: 1}
        chi_idx = chi_map.get(lunar_month, 2)

        # Can tháng: Ngũ Hổ Độn từ Can năm
        year_pillar = self.get_year_pillar(year)
        year_can = year_pillar["can"]
        base = HOUR_CAN_BASE.get(year_can, 0)  # Dùng lại bảng tương tự
        # Bảng Ngũ Hổ Độn tháng:
        month_can_base = {
            "Giáp": 2, "Kỷ": 2,    # Tháng Dần bắt đầu bằng Bính
            "Ất": 4, "Canh": 4,    # Bắt đầu bằng Mậu
            "Bính": 6, "Tân": 6,   # Bắt đầu bằng Canh
            "Đinh": 8, "Nhâm": 8,  # Bắt đầu bằng Nhâm
            "Mậu": 0, "Quý": 0,    # Bắt đầu bằng Giáp
        }
        can_start = month_can_base.get(year_can, 0)
        can_idx = (can_start + (chi_idx - 2)) % 10  # Dần là tháng 1

        chi = DIA_CHI[chi_idx]
        can = THIEN_CAN[can_idx % 10]
        return self._build_pillar(can, chi)

    # ── Trụ Ngày ─────────────────────────────────────────────────────────────
    def get_day_pillar(self, year: int, month: int, day: int) -> Dict:
        """
        Công thức tính Can Chi ngày chuẩn:
        Số ngày Julian → mod 60 → Can & Chi
        """
        jd = self._julian_day(year, month, day)
        # Mốc: JD 2299161 = 15/10/1582 = Giáp Tý
        # Thực tế mốc thường dùng: JD mod 60
        # Giáp Tý = JD 2451096 (ngày 8/1/1999)
        offset = jd - 2451096
        index = offset % 60
        if index < 0:
            index += 60
        can_idx = int(index) % 10
        chi_idx = int(index) % 12
        can = THIEN_CAN[can_idx]
        chi = DIA_CHI[chi_idx]
        return self._build_pillar(can, chi)

    def _julian_day(self, year: int, month: int, day: int) -> int:
        """Tính Julian Day Number."""
        a = (14 - month) // 12
        y = year + 4800 - a
        m = month + 12 * a - 3
        jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        return jdn

    # ── Trụ Giờ ─────────────────────────────────────────────────────────────
    def get_hour_pillar(self, hour: int, day_can: str) -> Dict:
        """
        Tính Trụ Giờ theo Ngũ Thử Độn (dựa vào Can ngày).
        """
        chi = HOUR_TO_CHI.get(hour, "Tý")
        chi_idx = DIA_CHI.index(chi)

        # Bảng Ngũ Thử Độn giờ:
        hour_can_base_table = {
            "Giáp": 0, "Kỷ": 0,    # Giờ Tý Can = Giáp
            "Ất": 2, "Canh": 2,    # Giờ Tý Can = Bính
            "Bính": 4, "Tân": 4,   # Giờ Tý Can = Mậu
            "Đinh": 6, "Nhâm": 6,  # Giờ Tý Can = Canh
            "Mậu": 8, "Quý": 8,    # Giờ Tý Can = Nhâm
        }
        can_start = hour_can_base_table.get(day_can, 0)
        can_idx = (can_start + chi_idx) % 10
        can = THIEN_CAN[can_idx]
        return self._build_pillar(can, chi)

    # ── Build Pillar Dict ────────────────────────────────────────────────────
    def _build_pillar(self, can: str, chi: str) -> Dict:
        return {
            "can": can,
            "chi": chi,
            "can_hanh": CAN_HANH[can],
            "chi_hanh": CHI_HANH[chi],
            "can_am_duong": CAN_AM_DUONG[can],
            "chi_am_duong": CHI_AM_DUONG[chi],
            "tang_can": TANG_CAN.get(chi, []),
            "ngu_hanh": CAN_HANH[can],  # Ngũ hành chủ = Can
        }

    # ── Tổng hợp Tứ Trụ ─────────────────────────────────────────────────────
    def calculate(self, birth_dt: datetime, gender: str) -> Dict:
        year = birth_dt.year
        month = birth_dt.month
        day = birth_dt.day
        hour = birth_dt.hour

        year_p = self.get_year_pillar(year)
        month_p = self.get_month_pillar(year, month, day)
        day_p = self.get_day_pillar(year, month, day)
        hour_p = self.get_hour_pillar(hour, day_p["can"])

        # Nhật Chủ = Can ngày
        nhat_chu = day_p["can"]
        nhat_chu_hanh = CAN_HANH[nhat_chu]

        # Mệnh theo Can năm
        menh = MENH_MAP.get(year_p["can"], "Mộc")

        # Tính Dụng Thần & Kỵ Thần (simplified)
        dung_than, ky_than = self._calc_dung_ky_than(nhat_chu_hanh, year_p, month_p, day_p, hour_p)

        return {
            "year_pillar": year_p,
            "month_pillar": month_p,
            "day_pillar": day_p,
            "hour_pillar": hour_p,
            "nhat_chu": nhat_chu,
            "nhat_chu_hanh": nhat_chu_hanh,
            "menh": menh,
            "ngu_hanh_chu": nhat_chu_hanh,
            "dung_than": dung_than,
            "ky_than": ky_than,
            "gender": gender,
        }

    def _calc_dung_ky_than(self, nhat_chu_hanh: str, *pillars) -> tuple:
        """
        Simplified Dụng Thần: dựa vào ngũ hành khắc và sinh.
        Kỵ Thần = hành khắc Nhật Chủ.
        Dụng Thần = hành sinh Nhật Chủ.
        """
        SINH_HANH = {
            "Mộc": "Thủy",  # Thủy sinh Mộc
            "Hỏa": "Mộc",
            "Thổ": "Hỏa",
            "Kim": "Thổ",
            "Thủy": "Kim",
        }
        dung_than = SINH_HANH.get(nhat_chu_hanh, "Thủy")
        ky_than = BI_KHAC_BOI.get(nhat_chu_hanh, "Kim")
        return dung_than, ky_than

    # ── Kiểm tra Xung / Khắc ─────────────────────────────────────────────────
    @staticmethod
    def is_xung_can(can1: str, can2: str) -> bool:
        return XUNG_CAN.get(can1) == can2

    @staticmethod
    def is_xung_chi(chi1: str, chi2: str) -> bool:
        return XUNG_CHI.get(chi1) == chi2

    @staticmethod
    def is_khac_hanh(hanh1: str, hanh2: str) -> bool:
        """hanh1 có khắc hanh2 không?"""
        return KHAC_HANH.get(hanh1) == hanh2

    @staticmethod
    def is_hinh(chi1: str, chi2: str) -> bool:
        return HINH_CHI.get(chi1) == chi2

    @staticmethod
    def is_hop_chi(chi1: str, chi2: str) -> bool:
        return HOP_CHI.get(chi1) == chi2

    @staticmethod
    def get_all_relations(pillar1: Dict, pillar2: Dict) -> Dict:
        """Phân tích đầy đủ quan hệ giữa 2 trụ."""
        can1, chi1 = pillar1["can"], pillar1["chi"]
        can2, chi2 = pillar2["can"], pillar2["chi"]
        h1, h2 = pillar1["can_hanh"], pillar2["can_hanh"]

        xung_can = TuTruCalculator.is_xung_can(can1, can2)
        xung_chi = TuTruCalculator.is_xung_chi(chi1, chi2)
        khac_hanh = TuTruCalculator.is_khac_hanh(h1, h2) or TuTruCalculator.is_khac_hanh(h2, h1)
        hinh = TuTruCalculator.is_hinh(chi1, chi2)
        hop = TuTruCalculator.is_hop_chi(chi1, chi2)

        score = 0
        details = []
        if xung_chi:
            score += 3
            details.append(f"Chi xung ({chi1}↔{chi2})")
        if xung_can:
            score += 2
            details.append(f"Can xung ({can1}↔{can2})")
        if khac_hanh:
            score += 2
            khac_dir = "khắc" if TuTruCalculator.is_khac_hanh(h1, h2) else "bị khắc"
            details.append(f"Ngũ hành {khac_dir} ({h1}↔{h2})")
        if hinh:
            score += 1
            details.append(f"Hình ({chi1}↔{chi2})")

        return {
            "xung_can": xung_can,
            "xung_chi": xung_chi,
            "khac_hanh": khac_hanh,
            "hinh": hinh,
            "hop": hop,
            "score": score,
            "details": details,
        }


# Exports dùng cho engine khác
__all__ = [
    "TuTruCalculator",
    "THIEN_CAN", "DIA_CHI",
    "CAN_HANH", "CHI_HANH",
    "XUNG_CHI", "XUNG_CAN",
    "KHAC_HANH", "BI_KHAC_BOI",
    "HINH_CHI", "HOP_CHI",
    "TANG_CAN", "MENH_MAP",
]
