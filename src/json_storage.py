import json
import os
from typing import Any

from src.abc_storage import ABCStorage
from src.aeroplane import Aeroplane


class JSONStorage(ABCStorage):
    """Класс для сохранения информации о самолетах в JSON-файл."""

    def __init__(self, file_path: str = "data/aeroplanes.json") -> None:
        """
        Инициализирует хранилище с указанным путём к JSON-файлу.
        Args:
            file_path (str): Путь к файлу для хранения данных. По умолчанию "data/aeroplanes.json"
        """
        self.file_path = file_path
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Создаёт директорию для файла, если она не существует."""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _load_data(self) -> list[dict[str, Any]]:
        """
        Загружает данные из JSON-файла.
        Returns:
            list[dict[str, Any]]: Список словарей с данными о самолётах.
                                  Если файл не найден или повреждён, возвращает пустой список.
        """
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: list[dict[str, Any]]) -> None:
        """
        Сохраняет данные в JSON-файл.
        Args:
            data (list[dict[str, Any]]): Данные для сохранения
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except TypeError as e:
            print(f"Ошибка при сохранении данных: {e}")

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Добавляет или обновляет информацию о самолёте в хранилище.
        Если самолёт с таким ICAO-кодом уже существует, он обновляется.
        Иначе добавляется новый.
        Args:
            aeroplane (Aeroplane): Объект самолёта для добавления или обновления
        """
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
        """
        Возвращает список самолётов, соответствующих критериям фильтрации.
        Args:
            **criteria: Критерии фильтрации (например, origin_country="United States")
        Returns:
            list[Aeroplane]: Список объектов самолётов, соответствующих критериям.
                             Если критерии не указаны, возвращает все самолёты.
        """
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
        """
        Удаляет самолёт из хранилища по ICAO-коду.
        Args:
            aeroplane (Aeroplane): Объект самолёта для удаления
        """
        data = self._load_data()
        data = [item for item in data if item.get("icao24") != aeroplane.icao24]
        self._save_data(data)

    def delete_by_criteria(self, **criteria: Any) -> None:
        """
        Удаляет самолёты по указанным критериям.
        Args:
            **criteria: Критерии для удаления.
        Примеры:
            storage.delete_by_criteria(origin_country="United States")
            storage.delete_by_criteria(on_ground=True)
        """
        if not criteria:
            return

        data = self._load_data()

        # Оставляем только те записи, которые НЕ подходят под критерии
        filtered_data = []
        for item in data:
            match = False
            for key, value in criteria.items():
                if item.get(key) == value:
                    match = True
                    break
            if not match:
                filtered_data.append(item)

        self._save_data(filtered_data)

    def clear(self) -> None:
        """Полностью очищает хранилище"""
        self._save_data([])

    def get_all(self) -> list[Aeroplane]:
        """
        Возвращает все самолёты из хранилища.
        Returns:
            list[Aeroplane]: Список всех объектов самолётов в хранилище
        """
        return self.get_aeroplanes()

    def count(self) -> int:
        """
        Возвращает количество записей в хранилище.
        Returns:
            int: Количество самолётов в хранилище
        """
        data = self._load_data()
        return len(data)