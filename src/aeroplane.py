from typing import Any


class Aeroplane:
    """
    Класс для работы с информацией о самолетах.
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
        current_country: str = "Неизвестно",  # ← НОВЫЙ АТРИБУТ
    ) -> None:
        self.icao24 = icao24
        self._callsign = callsign
        self._origin_country = origin_country
        self._velocity = self._validate_velocity(velocity)
        self._baro_altitude = self._validate_altitude(baro_altitude)
        self._longitude = longitude
        self._latitude = latitude
        self._on_ground = on_ground
        self._current_country = current_country  # ← НОВЫЙ АТРИБУТ

    # ========== Валидация ==========

    @staticmethod
    def _validate_velocity(velocity: float | None) -> float:
        if velocity is None:
            return 0.0
        if velocity < 0:
            return 0.0
        return velocity

    @staticmethod
    def _validate_altitude(altitude: float | None) -> float:
        if altitude is None:
            return 0.0
        if altitude < 0:
            return 0.0
        return altitude

    # ========== Геттеры и сеттеры ==========

    @property
    def callsign(self) -> str:
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Позывной/наименование не может быть пустым")
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
        if value < 0:
            self._velocity = 0.0
        else:
            self._velocity = value

    @property
    def baro_altitude(self) -> float:
        return self._baro_altitude

    @baro_altitude.setter
    def baro_altitude(self, value: float) -> None:
        if value < 0:
            self._baro_altitude = 0.0
        else:
            self._baro_altitude = value

    @property
    def longitude(self) -> float | None:
        return self._longitude

    @property
    def latitude(self) -> float | None:
        return self._latitude

    @property
    def on_ground(self) -> bool:
        return self._on_ground

    @property
    def current_country(self) -> str:  # ← НОВЫЙ ГЕТТЕР
        return self._current_country

    @current_country.setter
    def current_country(self, value: str) -> None:
        self._current_country = value

    # ========== Методы сравнения ==========

    def __lt__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity < other.velocity

    def __le__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity <= other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity > other.velocity

    def __ge__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity >= other.velocity

    def compare_altitude(self, other: "Aeroplane") -> int:
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только объекты Aeroplane")

        if self.baro_altitude > other.baro_altitude:
            return 1
        elif self.baro_altitude < other.baro_altitude:
            return -1
        else:
            return 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.icao24 == other.icao24

    def __str__(self) -> str:
        return (
            f"Самолет {self.callsign}\n"
            f"  Страна регистрации: {self.origin_country}\n"
            f"  Где летит сейчас: {self.current_country}\n"  # ← НОВАЯ СТРОКА
            f"  Скорость: {self.velocity:.1f} м/с\n"
            f"  Высота: {self.baro_altitude:.1f} м\n"
            f"  ICAO: {self.icao24}\n"
            f"  Координаты: {self.latitude}, {self.longitude}\n"
            f"  На земле: {'Да' if self.on_ground else 'Нет'}"
        )

    def __repr__(self) -> str:
        return (
            f"Aeroplane(callsign='{self.callsign}', "
            f"origin_country='{self.origin_country}', "
            f"current_country='{self.current_country}', "
            f"velocity={self.velocity}, "
            f"baro_altitude={self.baro_altitude})"
        )

    # ========== Методы для работы с данными ==========

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Aeroplane":
        return cls(
            callsign=data.get("callsign", "Неизвестно"),
            origin_country=data.get("origin_country", "Неизвестно"),
            velocity=data.get("velocity"),
            baro_altitude=data.get("baro_altitude"),
            longitude=data.get("longitude"),
            latitude=data.get("latitude"),
            icao24=data.get("icao24", "Неизвестно"),
            on_ground=data.get("on_ground", False),
            current_country=data.get("current_country", "Неизвестно"),  # ← НОВОЕ
        )

    @classmethod
    def cast_to_object_list(
        cls, data_list: list[dict[str, Any]], country: str = "Неизвестно"
    ) -> list["Aeroplane"]:
        """
        Преобразует список словарей в список объектов Aeroplane.

        Args:
            data_list (list[dict[str, Any]]): Список словарей с данными
            country (str): Текущая страна (для заполнения current_country)

        Returns:
            list[Aeroplane]: Список объектов самолетов
        """
        aeroplanes = []
        for data in data_list:
            data["current_country"] = country  # ← Добавляем страну
            aeroplanes.append(cls.from_dict(data))
        return aeroplanes

    def to_dict(self) -> dict[str, Any]:
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "current_country": self.current_country,  # ← НОВОЕ
            "velocity": self.velocity if self.velocity is not None else 0.0,
            "baro_altitude": self.baro_altitude if self.baro_altitude is not None else 0.0,
            "longitude": self.longitude if self.longitude is not None else 0.0,
            "latitude": self.latitude if self.latitude is not None else 0.0,
            "on_ground": self.on_ground if self.on_ground is not None else False,
        }
