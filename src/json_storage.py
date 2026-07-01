import json
import os
from typing import Any

from src.aeroplane import Aeroplane


class JSONStorage:
    """Класс для сохранения информации о самолетах в JSON-файл."""

    def __init__(self, file_path: str = "data/aeroplanes.json") -> None:
        self.file_path = file_path
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _load_data(self) -> list[dict[str, Any]]:
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: list[dict[str, Any]]) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except TypeError as e:
            print(f"Ошибка при сохранении данных: {e}")
            print("Проверьте, что все значения могут быть сериализованы в JSON")

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load_data()
        aeroplane_dict = aeroplane.to_dict()

        for i, item in enumerate(data):
            if item.get("icao24") == aeroplane.icao24:
                data[i] = aeroplane_dict
                self._save_data(data)
                return

        data.append(aeroplane_dict)
        self._save_data(data)

    def get_aeroplanes(self, **criteria: Any) -> list[Aeroplane]:
        data = self._load_data()

        if not data:
            return []

        if not criteria:
            return [Aeroplane.from_dict(item) for item in data]

        filtered = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                filtered.append(Aeroplane.from_dict(item))

        return filtered

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load_data()
        data = [item for item in data if item.get("icao24") != aeroplane.icao24]
        self._save_data(data)

    def clear(self) -> None:
        self._save_data([])

    def get_all(self) -> list[Aeroplane]:
        return self.get_aeroplanes()

    def count(self) -> int:
        data = self._load_data()
        return len(data)