from typing import Any, Dict, Union, Iterable

import requests

from src.abc_api import ABCAPI


class APIAdapter(ABCAPI):
    """
    Класс для работы с API сервисами:
    - nominatim.openstreetmap.org (получение координат стран)
    - opensky-network.org (получение информации о самолетах)
    """

    def __init__(self) -> None:
        """Инициализация с базовыми URL для API"""
        self._openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self._opensky_url = "https://opensky-network.org/api/states/all"
        self._timeout = 15
        self._user_agent = "coursework-app/1.0"
        self._aeroplanes: list[dict[str, Any]] = []

    def get_country_coordinates(self, country_name: str) -> list[float]:
        """
        Получает boundingbox страны через nominatim API.

        Args:
            country_name (str): Название страны

        Returns:
            list[float]: [широта_юг, широта_север, долгота_запад, долгота_восток]

        Raises:
            ValueError: Если страна не найдена
            ConnectionError: Если ошибка при запросе
        """
        if not country_name or not country_name.strip():
            raise ValueError("Название страны не может быть пустым")

        headers = {
            "User-Agent": self._user_agent,
        }

        params: Dict[str, Union[str, int, float]] = {
            "q": country_name,
            "format": "json",
            "limit": 1,
        }

        try:
            response = requests.get(
                self._openstreetmap_url,
                params=params,
                headers=headers,
                timeout=self._timeout
            )
            response.raise_for_status()

            data = response.json()

            if not data:
                raise ValueError(f"Страна '{country_name}' не найдена")

            boundingbox = data[0].get("boundingbox", [])

            if not boundingbox or len(boundingbox) != 4:
                raise ValueError(f"Не удалось получить координаты для '{country_name}'")

            return [float(coord) for coord in boundingbox]

        except requests.exceptions.Timeout:
            raise ConnectionError("Превышено время ожидания при запросе к API")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к nominatim API: {e}")

    def get_aeroplanes(self, country_name: str) -> list[dict[str, Any]]:
        """
        Получает информацию о самолетах в воздушном пространстве страны.

        Args:
            country_name (str): Название страны

        Returns:
            list[dict[str, Any]]: Список словарей с данными о самолетах
        """
        # Получаем координаты страны
        bbox = self.get_country_coordinates(country_name)

        # Используем bounding box для получения самолетов
        return self.get_aeroplanes_by_bounding_box(bbox)

    def get_aeroplanes_by_bounding_box(self, bbox: list[float]) -> list[dict[str, Any]]:
        """
        Получает информацию о самолетах по заданному bounding box.

        Args:
            bbox (list[float]): [юг, север, запад, восток]

        Returns:
            list[dict[str, Any]]: Список словарей с данными о самолетах

        Raises:
            ValueError: Если bbox некорректный
            ConnectionError: Если ошибка при запросе к API
        """
        if not bbox or len(bbox) != 4:
            raise ValueError("Некорректный bounding box. Ожидается [юг, север, запад, восток]")

        # Проверяем корректность координат
        for coord in bbox:
            if not isinstance(coord, (int, float)):
                raise ValueError("Все координаты должны быть числами")

        params = {
            "lamin": bbox[0],  # юг (min latitude)
            "lamax": bbox[1],  # север (max latitude)
            "lomin": bbox[2],  # запад (min longitude)
            "lomax": bbox[3],  # восток (max longitude)
        }

        try:
            response = requests.get(self._opensky_url, params=params, timeout=self._timeout)
            response.raise_for_status()

            data = response.json()
            states = data.get("states", [])

            if not states:
                return []

            self._aeroplanes = self._parse_states(states)
            return self._aeroplanes

        except requests.exceptions.Timeout:
            raise ConnectionError("Превышено время ожидания при запросе к opensky API")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к opensky API: {e}")
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Ошибка при обработке данных от opensky: {e}")

    def _parse_states(self, states: list[list]) -> list[dict[str, Any]]:
        """
        Парсит данные о самолетах из формата opensky.

        Формат ответа opensky (индексы в массиве):
        0: icao24 - ICAO-адрес транспондера
        1: callsign - Позывной (8 символов)
        2: origin_country - Страна регистрации
        3: time_position - Время получения позиции (Unix timestamp)
        4: last_contact - Время последнего контакта (Unix timestamp)
        5: longitude - Долгота
        6: latitude - Широта
        7: baro_altitude - Барометрическая высота (метры)
        8: on_ground - На земле (True/False)
        9: velocity - Скорость (м/с)
        10: true_track - Курс (градусы)
        11: vertical_rate - Вертикальная скорость (м/с)
        12: sensors - Датчики
        13: geo_altitude - Геометрическая высота (метры)
        14: squawk - Код Squawk
        15: spi - Special Purpose Indicator
        16: position_source - Источник позиции

        Args:
            states (list[list]): Список списков с данными от opensky

        Returns:
            list[dict[str, Any]]: Список словарей с данными о самолетах
        """
        aeroplanes = []

        for state in states:
            if not state or len(state) < 17:
                continue

            aeroplane = {
                "icao24": state[0] if state[0] else "Неизвестно",
                "callsign": state[1].strip() if state[1] else "Неизвестно",
                "origin_country": state[2] if state[2] else "Неизвестно",
                "time_position": state[3],
                "last_contact": state[4],
                "longitude": state[5],
                "latitude": state[6],
                "baro_altitude": state[7],
                "on_ground": state[8] if state[8] is not None else False,
                "velocity": state[9],
                "true_track": state[10],
                "vertical_rate": state[11],
                "sensors": state[12],
                "geo_altitude": state[13],
                "squawk": state[14],
                "spi": state[15],
                "position_source": state[16],
            }
            aeroplanes.append(aeroplane)

        return aeroplanes


# Для проверки работы
if __name__ == "__main__":
    api = APIAdapter()

    try:
        # Проверка координат
        coords = api.get_country_coordinates("Canada")
        print(f"Координаты Канады: {coords}")

        # Проверка самолетов
        planes = api.get_aeroplanes("Canada")
        print(f"Найдено самолетов: {len(planes)}")
        if planes:
            print(f"Первый самолет: {planes[0]}")
    except Exception as e:
        print(f"Ошибка: {e}")
