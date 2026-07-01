from abc import ABC, abstractmethod
from typing import Any


class ABCAPI(ABC):
    """
    Абстрактный класс для работы с API сервисами.
    Определяет интерфейс для получения координат стран и информации о самолетах.
    """

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> list[float]:        # pragma: no cover
        """
        Получает географические координаты страны.

        Args:
            country_name (str): Название страны

        Returns:
            list[float]: Список координат [широта_юг, широта_север, долгота_запад, долгота_восток]

        Raises:
            ValueError: Если страна не найдена
            ConnectionError: Если ошибка при запросе к API
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> list[dict[str, Any]]:        # pragma: no cover
        """
        Получает информацию о самолетах в воздушном пространстве страны.

        Args:
            country_name (str): Название страны

        Returns:
            list[dict[str, Any]]: Список словарей с данными о самолетах

        Raises:
            ValueError: Если страна не найдена
            ConnectionError: Если ошибка при запросе к API
        """
        pass

    @abstractmethod
    def get_aeroplanes_by_bounding_box(self, bbox: list[float]) -> list[dict[str, Any]]:    # pragma: no cover
        """
        Получает информацию о самолетах по заданному bounding box.

        Args:
            bbox (list[float]): Список координат [юг, север, запад, восток]

        Returns:
            list[dict[str, Any]]: Список словарей с данными о самолетах
        """
        pass