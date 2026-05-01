"""
core/profile.py — Lưu/đọc profile người dùng (JSON file)
"""

import json
import os
from typing import Optional, Dict


class ProfileManager:
    def __init__(self, filepath: str = "data/profiles.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load_all(self) -> Dict:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_all(self, data: Dict):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save(self, user_id: int, profile: Dict):
        """Lưu profile của user."""
        all_profiles = self._load_all()
        # Chuyển tutu sang serializable (datetime → string)
        profile_copy = dict(profile)
        all_profiles[str(user_id)] = profile_copy
        self._save_all(all_profiles)

    def load(self, user_id: int) -> Optional[Dict]:
        """Đọc profile của user. Trả về None nếu chưa có."""
        all_profiles = self._load_all()
        return all_profiles.get(str(user_id))

    def delete(self, user_id: int):
        """Xóa profile của user."""
        all_profiles = self._load_all()
        all_profiles.pop(str(user_id), None)
        self._save_all(all_profiles)

    def exists(self, user_id: int) -> bool:
        all_profiles = self._load_all()
        return str(user_id) in all_profiles
