"""
core/daiky.py — Engine tính Ngày Đại Kỵ
Logic: Xung/Khắc/Hình với Tứ Trụ + Đồng Pha 4 Khung + Lọc tháng
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import calendar


class DaiKyEngine:
    def __init__(self, tutu_calc, tietki_engine):
        self.tutu = tutu_calc
        self.tietki = tietki_engine

    # ─── Phân tích 1 ngày ────────────────────────────────────────────────────
    def analyze_day(self, user_tutu: Dict, dt: datetime) -> Dict:
        """
        Phân tích mức độ Đại Kỵ của một ngày cụ thể với Tứ Trụ người dùng.

        Trả về:
          level: 0=an toàn, 1=nhẹ, 2=trung, 3=nặng, 4=đồng pha 4 khung
          score: điểm xung khắc tổng
          reasons: danh sách lý do
          dongpha_detail: chi tiết từng trụ bị đồng pha
          can_chi: Can Chi ngày hôm đó
        """
        day_p = self.tutu.get_day_pillar(dt.year, dt.month, dt.day)
        can_chi = f"{day_p['can']} {day_p['chi']}"

        user_pillars = {
            "Năm": user_tutu["year_pillar"],
            "Tháng": user_tutu["month_pillar"],
            "Ngày": user_tutu["day_pillar"],
            "Giờ": user_tutu["hour_pillar"],
        }

        total_score = 0
        reasons = []
        pillar_scores = {}   # tên trụ → score
        pillar_details = {}  # tên trụ → [chi tiết]

        for pillar_name, user_p in user_pillars.items():
            rel = self.tutu.get_all_relations(day_p, user_p)
            pillar_scores[pillar_name] = rel["score"]
            pillar_details[pillar_name] = rel["details"]
            total_score += rel["score"]

            if rel["score"] >= 3:
                reasons.append(
                    f"Ngày {can_chi} xung khắc mạnh Trụ {pillar_name} "
                    f"({user_p['can']} {user_p['chi']}): " +
                    ", ".join(rel["details"])
                )
            elif rel["score"] >= 2:
                reasons.append(
                    f"Trụ {pillar_name} ({user_p['can']} {user_p['chi']}): " +
                    ", ".join(rel["details"])
                )

        # ── Đồng Pha 4 Khung ─────────────────────────────────────────────────
        # Tiêu chí: tất cả 4 trụ đều có score >= 2 (xung hoặc khắc)
        dongpha_pillars = [k for k, v in pillar_scores.items() if v >= 2]
        is_dongpha_4 = len(dongpha_pillars) == 4

        dongpha_detail = []
        if is_dongpha_4:
            for pname in dongpha_pillars:
                up = user_pillars[pname]
                detail_str = ", ".join(pillar_details[pname])
                dongpha_detail.append(
                    f"🔴 Trụ {pname} ({up['can']} {up['chi']}): {detail_str}"
                )

        # ── Phân mức độ ──────────────────────────────────────────────────────
        if is_dongpha_4:
            level = 4
        elif total_score >= 9:
            level = 3
        elif total_score >= 5:
            level = 2
        elif total_score >= 2:
            level = 1
        else:
            level = 0

        # Thêm phân tích Tiết Khí
        tietki_now = self.tietki.get_current_tietki(dt)
        nhat_chu_hanh = user_tutu["day_pillar"]["can_hanh"]
        vs = self.tietki.analyze_vuong_suy(nhat_chu_hanh, tietki_now["name"])

        # Nhật Chủ Tử trong tiết khí → cộng thêm điểm kỵ
        if vs["trang_thai"] == "Tử" and level >= 2:
            level = min(level + 1, 4)
            reasons.append(
                f"Nhật Chủ {user_tutu['day_pillar']['can']} ({nhat_chu_hanh}) "
                f"đang ở trạng thái TỬ trong tiết {tietki_now['name']}"
            )

        return {
            "date": dt.strftime("%d/%m/%Y"),
            "can_chi": can_chi,
            "level": level,
            "score": total_score,
            "reasons": reasons,
            "dongpha_detail": dongpha_detail,
            "is_dongpha_4": is_dongpha_4,
            "pillar_scores": pillar_scores,
            "tietki": tietki_now["name"],
            "vuong_suy": vs,
        }

    # ─── Lấy ngày đại kỵ của 1 tháng ────────────────────────────────────────
    def get_month_daiky(self, user_tutu: Dict, month: int, year: int,
                        min_level: int = 1) -> List[Dict]:
        """
        Trả về danh sách ngày đại kỵ trong tháng với level >= min_level.
        Bao gồm logic lọc tháng kỵ.
        """
        # Kiểm tra tháng kỵ
        month_ky_level = self._check_thang_ky(user_tutu, month, year)

        num_days = calendar.monthrange(year, month)[1]
        result = []

        for day in range(1, num_days + 1):
            dt = datetime(year, month, day)
            analysis = self.analyze_day(user_tutu, dt)

            # Nếu tháng đã kỵ, cộng thêm 1 bậc cho ngày kỵ
            effective_level = analysis["level"]
            if month_ky_level >= 2 and effective_level >= 1:
                effective_level = min(effective_level + 1, 4)
                analysis = dict(analysis)
                analysis["level"] = effective_level
                if month_ky_level >= 2:
                    analysis["reasons"] = analysis["reasons"] + [
                        f"Tháng {month} là tháng kỵ (cộng thêm 1 bậc)"
                    ]

            if effective_level >= min_level:
                result.append(analysis)

        return result

    # ─── Kiểm tra Tháng Kỵ ───────────────────────────────────────────────────
    def _check_thang_ky(self, user_tutu: Dict, month: int, year: int) -> int:
        """
        Kiểm tra mức độ kỵ của cả tháng dựa vào trụ tháng.
        Trả về: 0=bình thường, 1=nhẹ, 2=kỵ, 3=đại kỵ tháng
        """
        # Lấy Can Chi của tháng hiện tại
        month_p = self.tutu.get_month_pillar(year, month, 15)
        user_pillars = [
            user_tutu["year_pillar"],
            user_tutu["month_pillar"],
            user_tutu["day_pillar"],
            user_tutu["hour_pillar"],
        ]

        total = 0
        conflict_count = 0
        for up in user_pillars:
            rel = self.tutu.get_all_relations(month_p, up)
            total += rel["score"]
            if rel["score"] >= 2:
                conflict_count += 1

        if conflict_count == 4:
            return 3
        elif total >= 8:
            return 2
        elif total >= 4:
            return 1
        return 0

    # ─── Lấy ngày đại kỵ của cả năm ─────────────────────────────────────────
    def get_year_daiky(self, user_tutu: Dict, year: int,
                       min_level: int = 3) -> List[Dict]:
        """Trả về tất cả ngày đại kỵ nặng (level >= min_level) trong năm."""
        result = []
        for month in range(1, 13):
            days = self.get_month_daiky(user_tutu, month, year, min_level)
            result.extend(days)
        return result

    # ─── Tìm ngày đại kỵ trong khoảng ───────────────────────────────────────
    def get_daiky_in_range(self, user_tutu: Dict, start_dt: datetime,
                           end_dt: datetime, min_level: int = 3) -> List[Dict]:
        """Quét ngày đại kỵ trong khoảng thời gian."""
        result = []
        current = start_dt
        while current <= end_dt:
            analysis = self.analyze_day(user_tutu, current)
            if analysis["level"] >= min_level:
                result.append({**analysis, "datetime": current})
            current += timedelta(days=1)
        return result

    # ─── Đồng Pha 4 Khung chi tiết ───────────────────────────────────────────
    def get_dongpha_days(self, user_tutu: Dict, start_dt: datetime,
                         days_ahead: int = 90) -> List[Dict]:
        """Tìm tất cả ngày Đồng Pha 4 Khung trong khoảng thời gian."""
        result = []
        for i in range(days_ahead):
            dt = start_dt + timedelta(days=i)
            analysis = self.analyze_day(user_tutu, dt)
            if analysis["is_dongpha_4"]:
                result.append({**analysis, "datetime": dt})
        return result

    # ─── Thống kê Lọc Tháng & Ngày Giao Thoa ────────────────────────────────
    def get_thang_daiky_summary(self, user_tutu: Dict, year: int) -> List[Dict]:
        """
        Thống kê từng tháng: tháng kỵ + số ngày kỵ + level tháng.
        Dùng cho /ngaydaiky → xem tổng quan.
        """
        summary = []
        for month in range(1, 13):
            month_level = self._check_thang_ky(user_tutu, month, year)
            days = self.get_month_daiky(user_tutu, month, year, min_level=1)

            # Thống kê
            counts = {1: 0, 2: 0, 3: 0, 4: 0}
            for d in days:
                counts[d["level"]] = counts.get(d["level"], 0) + 1

            # Tiết khí tháng
            tietki_name = self.tietki.get_tietki_of_month(month, year)

            # Vượng Suy tháng đó
            nhat_chu_hanh = user_tutu["day_pillar"]["can_hanh"]
            vs = self.tietki.analyze_vuong_suy(nhat_chu_hanh, tietki_name)

            summary.append({
                "month": month,
                "year": year,
                "month_level": month_level,
                "tietki": tietki_name,
                "vuong_suy": vs,
                "day_counts": counts,
                "total_days": len(days),
            })

        return summary
