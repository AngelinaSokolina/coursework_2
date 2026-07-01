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

    def test_callsign_setter_whitespace(self) -> None:
        """Проверяет, что позывной из пробелов вызывает ошибку."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        with pytest.raises(ValueError, match="Позывной/наименование не может быть пустым"):
            plane.callsign = "   "

    def test_origin_country_setter_empty(self) -> None:
        """Проверяет, что пустая страна регистрации вызывает ошибку."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        with pytest.raises(ValueError, match="Страна регистрации не может быть пустой"):
            plane.origin_country = ""

    def test_origin_country_setter_whitespace(self) -> None:
        """Проверяет, что страна из пробелов вызывает ошибку."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        with pytest.raises(ValueError, match="Страна регистрации не может быть пустой"):
            plane.origin_country = "   "

    def test_current_country_setter(self) -> None:
        """Проверяет сеттер для текущей страны."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        plane.current_country = "France"
        assert plane.current_country == "France"

    def test_comparison_not_implemented(self) -> None:
        """Проверяет сравнение с объектом другого типа."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        with pytest.raises(TypeError):
            plane.compare_altitude("not a plane")  # type: ignore

    def test_compare_altitude_equal(self) -> None:
        """Проверяет сравнение равных высот."""
        plane1 = Aeroplane("A", "US", 100, 5000)
        plane2 = Aeroplane("B", "US", 200, 5000)
        assert plane1.compare_altitude(plane2) == 0

    def test_eq_different_type(self) -> None:
        """Проверяет сравнение с объектом другого типа."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        assert plane.__eq__("not a plane") is NotImplemented

    def test_to_dict(self) -> None:
        """Проверяет преобразование в словарь."""
        plane = Aeroplane(
            callsign="TEST123",
            origin_country="United States",
            velocity=250.5,
            baro_altitude=10000.0,
            longitude=10.5,
            latitude=20.5,
            icao24="abc123",
            on_ground=False,
            current_country="France"
        )
        data = plane.to_dict()

        assert data["callsign"] == "TEST123"
        assert data["origin_country"] == "United States"
        assert data["current_country"] == "France"
        assert data["velocity"] == 250.5
        assert data["baro_altitude"] == 10000.0
        assert data["longitude"] == 10.5
        assert data["latitude"] == 20.5
        assert data["icao24"] == "abc123"
        assert data["on_ground"] is False

    def test_from_dict_with_current_country(self) -> None:
        """Проверяет создание из словаря с current_country."""
        data = {
            "callsign": "SWR123",
            "origin_country": "Switzerland",
            "velocity": 280.5,
            "baro_altitude": 11000.0,
            "current_country": "Germany"
        }
        plane = Aeroplane.from_dict(data)
        assert plane.current_country == "Germany"

    def test_cast_to_object_list(self) -> None:
        """Проверяет преобразование списка словарей в объекты."""
        data_list = [
            {
                "callsign": "TEST1",
                "origin_country": "US",
                "velocity": 100,
                "baro_altitude": 5000
            },
            {
                "callsign": "TEST2",
                "origin_country": "FR",
                "velocity": 200,
                "baro_altitude": 10000
            }
        ]
        planes = Aeroplane.cast_to_object_list(data_list, "France")

        assert len(planes) == 2
        assert planes[0].current_country == "France"
        assert planes[1].current_country == "France"

    def test_repr(self) -> None:
        """Проверяет repr представление."""
        plane = Aeroplane("TEST", "US", 100, 5000, current_country="France")
        repr_str = repr(plane)
        assert "TEST" in repr_str
        assert "US" in repr_str
        assert "France" in repr_str
        assert "100" in repr_str
        assert "5000" in repr_str