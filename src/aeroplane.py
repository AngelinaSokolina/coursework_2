from typing import Any


class Aeroplane:
    """
    Класс для работы с информацией о самолетах.

    Атрибуты:
    - origin_country (str): Страна регистрации
    - callsign (str): Позывной
    - velocity (float): Скорость полета (м/с)
    - baro_altitude (float): Барометрическая высота (м)
    - icao24 (str): ICAO-адрес транспондера
    - longitude (float): Долгота
    - latitude (float): Широта
    - on_ground (bool): На земле или в воздухе
    """

    def __init__(
            self,
            callsign: str,
            origin_country: str,
            velocity: float | None,
            baro_altitude: float | None,
            longitude: float | None = None,
            latitude: float | None = None,
            icao24: str = "Неизвестно",
            on_ground: bool = False,
    ) -> None:
        """
        Инициализация самолета.

        Args:
            callsign (str): Позывной самолета
            origin_country (str): Страна регистрации
            velocity (float | None): Скорость полета (м/с)
            baro_altitude (float | None): Барометрическая высота (м)
            longitude (float | None): Долгота
            latitude (float | None): Широта
            icao24 (str): ICAO-адрес транспондера
            on_ground (bool): На земле ли самолет
        """
        self.icao24 = icao24
        self._callsign = callsign
        self._origin_country = origin_country
        self._velocity = self._validate_velocity(velocity)
        self._baro_altitude = self._validate_altitude(baro_altitude)
        self._longitude = longitude
        self._latitude = latitude
        self._on_ground = on_ground

    # ========== Валидация ==========

    @staticmethod
    def _validate_velocity(velocity: float | None) -> float:
        """Валидация скорости (должна быть >= 0)."""
        if velocity is None:
            return 0.0
        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        return velocity

    @staticmethod
    def _validate_altitude(altitude: float | None) -> float:
        """Валидация высоты (должна быть >= 0)."""
        if altitude is None:
            return 0.0
        if altitude < 0:
            raise ValueError("Высота не может быть отрицательной")
        return altitude

    # ========== Геттеры и сеттеры (инкапсуляция) ==========

    @property
    def callsign(self) -> str:
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Позывной не может быть пустым")
        self._callsign = value

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @origin_country.setter
    def origin_country(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Страна регистрации не может быть пустой")
        self._origin_country = value

    @property
    def velocity(self) -> float:
        return self._velocity

    @velocity.setter
    def velocity(self, value: float) -> None:
        self._velocity = self._validate_velocity(value)

    @property
    def baro_altitude(self) -> float:
        return self._baro_altitude

    @baro_altitude.setter
    def baro_altitude(self, value: float) -> None:
        self._baro_altitude = self._validate_altitude(value)

    @property
    def longitude(self) -> float | None:
        return self._longitude

    @property
    def latitude(self) -> float | None:
        return self._latitude

    @property
    def on_ground(self) -> bool:
        return self._on_ground

    # ========== Методы сравнения по скорости ==========

    def __lt__(self, other: "Aeroplane") -> bool:
        """Меньше по скорости."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity < other.velocity

    def __le__(self, other: "Aeroplane") -> bool:
        """Меньше или равно по скорости."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity <= other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        """Больше по скорости."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity > other.velocity

    def __ge__(self, other: "Aeroplane") -> bool:
        """Больше или равно по скорости."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity >= other.velocity

    # ========== Методы сравнения по высоте ==========

    def __lt__(self, other: "Aeroplane") -> bool:
        """Меньше по высоте."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.baro_altitude < other.baro_altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """Больше по высоте."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.baro_altitude > other.baro_altitude

    def compare_altitude(self, other: "Aeroplane") -> int:
        """
        Сравнивает два самолета по высоте.

        Returns:
            int: 1 если текущий выше, -1 если ниже, 0 если равны
        """
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только объекты Aeroplane")

        if self.baro_altitude > other.baro_altitude:
            return 1
        elif self.baro_altitude < other.baro_altitude:
            return -1
        else:
            return 0

    # ========== Другие методы ==========

    def __eq__(self, other: object) -> bool:
        """Сравнение по ICAO-коду."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.icao24 == other.icao24

    def __str__(self) -> str:
        """Строковое представление для пользователя."""
        return (
            f"Самолет {self.callsign}\n"
            f"  Страна регистрации: {self.origin_country}\n"
            f"  Скорость: {self.velocity:.1f} м/с\n"
            f"  Высота: {self.baro_altitude:.1f} м\n"
            f"  ICAO: {self.icao24}\n"
            f"  Координаты: {self.latitude}, {self.longitude}\n"
            f"  На земле: {'Да' if self.on_ground else 'Нет'}"
        )

    def __repr__(self) -> str:
        """Строковое представление для разработчика."""
        return (
            f"Aeroplane(callsign='{self.callsign}', "
            f"origin_country='{self.origin_country}', "
            f"velocity={self.velocity}, "
            f"baro_altitude={self.baro_altitude})"
        )

    # ========== Методы для работы с данными ==========

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Aeroplane":
        """
        Создает объект Aeroplane из словаря.

        Args:
            data (dict[str, Any]): Словарь с данными самолета

        Returns:
            Aeroplane: Объект самолета
        """
        return cls(
            callsign=data.get("callsign", "Неизвестно"),
            origin_country=data.get("origin_country", "Неизвестно"),
            velocity=data.get("velocity"),
            baro_altitude=data.get("baro_altitude"),
            longitude=data.get("longitude"),
            latitude=data.get("latitude"),
            icao24=data.get("icao24", "Неизвестно"),
            on_ground=data.get("on_ground", False),
        )

    @classmethod
    def cast_to_object_list(cls, data_list: list[dict[str, Any]]) -> list["Aeroplane"]:
        """
        Преобразует список словарей в список объектов Aeroplane.

        Args:
            data_list (list[dict[str, Any]]): Список словарей с данными

        Returns:
            list[Aeroplane]: Список объектов самолетов
        """
        return [cls.from_dict(data) for data in data_list]

    def to_dict(self) -> dict[str, Any]:
        """
        Преобразует объект в словарь для сохранения в JSON.

        Returns:
            dict[str, Any]: Словарь с данными самолета
        """
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "baro_altitude": self.baro_altitude,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "on_ground": self.on_ground,
        }


# ========== Демонстрация работы ==========

if __name__ == "__main__":
    # Создание самолетов
    plane1 = Aeroplane(
        callsign="UAL1621",
        origin_country="United States",
        velocity=268.79,
        baro_altitude=10203.18,
        icao24="abc123"
    )

    plane2 = Aeroplane(
        callsign="AFR123",
        origin_country="France",
        velocity=250.0,
        baro_altitude=9500.0,
        icao24="def456"
    )

    # Вывод информации
    print(plane1)
    print("\n" + "-" * 40 + "\n")
    print(plane2)

    # Сравнение по скорости
    print(f"\nСкорость plane1 > plane2: {plane1 > plane2}")  # True

    # Сравнение по высоте
    print(f"plane1 выше plane2: {plane1.compare_altitude(plane2)}")  # 1

    # Проверка валидации
    try:
        invalid_plane = Aeroplane("TEST", "Russia", -100, 10000)
    except ValueError as e:
        print(f"\nОшибка валидации: {e}")

    # Преобразование из словаря
    data = {
        "callsign": "SWR123",
        "origin_country": "Switzerland",
        "velocity": 280.5,
        "baro_altitude": 11000.0,
    }
    plane3 = Aeroplane.from_dict(data)
    print(f"\nСоздан из словаря: {plane3}")