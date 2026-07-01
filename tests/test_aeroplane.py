import pytest
from src.aeroplane import Aeroplane


class TestAeroplane:

    def test_aeroplane_init(self) -> None:
        """Проверяет инициализацию самолета."""
        plane = Aeroplane(
            callsign="UAL1621",
            origin_country="United States",
            velocity=268.79,
            baro_altitude=10203.18,
            longitude=10.0,
            latitude=20.0,
            icao24="abc123",
            on_ground=False,
            current_country="France",
        )
        assert plane.callsign == "UAL1621"
        assert plane.velocity == 268.79
        assert plane.current_country == "France"

    def test_aeroplane_init_with_none_values(self) -> None:
        """Проверяет инициализацию с None значениями."""
        plane = Aeroplane("TEST", "Test", None, None)
        assert plane.velocity == 0.0
        assert plane.baro_altitude == 0.0
        assert plane.icao24 == "Неизвестно"
        assert plane.current_country == "Неизвестно"

    def test_velocity_validation_negative(self) -> None:
        """Проверяет, что отрицательная скорость заменяется на 0."""
        plane = Aeroplane("TEST", "Test", -100, 10000)
        assert plane.velocity == 0.0

    def test_altitude_validation_negative(self) -> None:
        """Проверяет, что отрицательная высота заменяется на 0."""
        plane = Aeroplane("TEST", "Test", 100, -100)
        assert plane.baro_altitude == 0.0

    def test_velocity_setter(self) -> None:
        """Проверяет сеттер для скорости."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        plane.velocity = 200
        assert plane.velocity == 200
        plane.velocity = -50
        assert plane.velocity == 0.0

    def test_callsign_setter_empty(self) -> None:
        """Проверяет, что пустой позывной вызывает ошибку."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        with pytest.raises(ValueError, match="Позывной/наименование не может быть пустым"):
            plane.callsign = ""

    def test_comparison_by_velocity(self) -> None:
        """Проверяет сравнение по скорости."""
        plane1 = Aeroplane("A", "US", 100, 10000)
        plane2 = Aeroplane("B", "US", 200, 10000)
        assert plane1 < plane2
        assert plane2 > plane1

    def test_compare_altitude(self) -> None:
        """Проверяет сравнение по высоте."""
        plane1 = Aeroplane("A", "US", 100, 5000)
        plane2 = Aeroplane("B", "US", 200, 10000)
        assert plane1.compare_altitude(plane2) == -1

    def test_from_dict(self) -> None:
        """Проверяет создание объекта из словаря."""
        data = {"callsign": "SWR123", "origin_country": "Switzerland", "velocity": 280.5, "baro_altitude": 11000.0}
        plane = Aeroplane.from_dict(data)
        assert plane.callsign == "SWR123"
        assert plane.velocity == 280.5