from typing import Any


class Aeroplane:
    """
    Класс для работы с информацией о самолетах.
    """

    __slots__ = (
        "icao24",
        "_callsign",
        "_origin_country",
        "_velocity",
        "_baro_altitude",
        "_longitude",
        "_latitude",
        "_on_ground",
        "_current_country",
    )

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
        """
        Проверяет и нормализует значение скорости.
        Args:
            velocity (float | None): Скорость в м/с
        Returns:
            float: 0.0 если скорость None или отрицательная, иначе скорость
        """
        if velocity is None:
            return 0.0
        if velocity < 0:
            return 0.0
        return velocity

    @staticmethod
    def _validate_altitude(altitude: float | None) -> float:
        """
        Проверяет и нормализует значение высоты.
        Args:
            altitude (float | None): Высота в метрах
        Returns:
            float: 0.0 если высота None или отрицательная, иначе высота
        """
        if altitude is None:
            return 0.0
        if altitude < 0:
            return 0.0
        return altitude

    # ========== Геттеры и сеттеры ==========

    @property
    def callsign(self) -> str:
        """Возвращает позывной самолёта"""
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        """
        Устанавливает позывной самолёта.
        Args:
            value (str): Новый позывной
        Raises:
            ValueError: Если позывной пустой или состоит только из пробелов
        """
        if not value or not value.strip():
            raise ValueError("Позывной/наименование не может быть пустым")
        self._callsign = value

    @property
    def origin_country(self) -> str:
        """Возвращает страну регистрации самолёта"""
        return self._origin_country

    @origin_country.setter
    def origin_country(self, value: str) -> None:
        """
        Устанавливает страну регистрации самолёта.
        Args:
            value (str): Новая страна регистрации
        Raises:
            ValueError: Если страна пустая или состоит только из пробелов
        """
        if not value or not value.strip():
            raise ValueError("Страна регистрации не может быть пустой")
        self._origin_country = value

    @property
    def velocity(self) -> float:
        """Возвращает скорость самолёта в м/с"""
        return self._velocity

    @velocity.setter
    def velocity(self, value: float) -> None:
        """
        Устанавливает скорость самолёта.
        Args:
            value (float): Скорость в м/с
        """
        if value < 0:
            self._velocity = 0.0
        else:
            self._velocity = value

    @property
    def baro_altitude(self) -> float:
        """Возвращает барометрическую высоту самолёта в метрах"""
        return self._baro_altitude

    @baro_altitude.setter
    def baro_altitude(self, value: float) -> None:
        """
        Устанавливает барометрическую высоту самолёта.
        Args:
            value (float): Высота в метрах
        """
        if value < 0:
            self._baro_altitude = 0.0
        else:
            self._baro_altitude = value

    @property
    def longitude(self) -> float | None:
        """Возвращает долготу самолёта"""
        return self._longitude

    @property
    def latitude(self) -> float | None:
        """Возвращает широту самолёта"""
        return self._latitude

    @property
    def on_ground(self) -> bool:
        """Возвращает True, если самолёт находится на земле"""
        return self._on_ground

    @property
    def current_country(self) -> str:
        """Возвращает страну, над которой сейчас летит самолёт"""
        return self._current_country

    @current_country.setter
    def current_country(self, value: str) -> None:
        """
        Устанавливает текущую страну самолёта.
        Args:
            value (str): Название страны
        """
        self._current_country = value

    # ========== Методы сравнения ==========

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнивает два самолёта по скорости (меньше)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity < other.velocity

    def __le__(self, other: "Aeroplane") -> bool:
        """Сравнивает два самолёта по скорости (меньше или равно)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity <= other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнивает два самолёта по скорости (больше)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity > other.velocity

    def __ge__(self, other: "Aeroplane") -> bool:
        """Сравнивает два самолёта по скорости (больше или равно)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity >= other.velocity

    def compare_altitude(self, other: "Aeroplane") -> int:
        """
        Сравнивает два самолёта по высоте.
        Args:
            other (Aeroplane): Другой самолёт
        Returns:
            int: 1 если выше, -1 если ниже, 0 если равны
        Raises:
            TypeError: Если передан не объект Aeroplane
        """
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только объекты Aeroplane")

        if self.baro_altitude > other.baro_altitude:
            return 1
        elif self.baro_altitude < other.baro_altitude:
            return -1
        else:
            return 0

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает два самолёта по ICAO-коду.
        Args:
            other (object): Другой объект
        Returns:
            bool: True если ICAO-коды совпадают
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.icao24 == other.icao24

    def __str__(self) -> str:
        """
        Возвращает строковое представление самолёта для пользователя.
        Returns:
            str: Форматированная строка с информацией о самолёте
        """
        return (
            f"Самолет {self.callsign}\n"
            f"  Страна регистрации: {self.origin_country}\n"
            f"  Где летит сейчас: {self.current_country}\n"
            f"  Скорость: {self.velocity:.1f} м/с\n"
            f"  Высота: {self.baro_altitude:.1f} м\n"
            f"  ICAO: {self.icao24}\n"
            f"  Координаты: {self.latitude}, {self.longitude}\n"
            f"  На земле: {'Да' if self.on_ground else 'Нет'}"
        )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление самолёта для разработчиков.
        Returns:
            str: Строка для отладки
        """
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
        """
        Создаёт объект Aeroplane из словаря.
        Args:
            data (dict[str, Any]): Словарь с данными самолёта
        Returns:
            Aeroplane: Новый объект самолёта
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
            current_country=data.get("current_country", "Неизвестно"),
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
