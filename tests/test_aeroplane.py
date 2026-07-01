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
        assert plane.origin_country == "United States"
        assert plane.velocity == 268.79
        assert plane.baro_altitude == 10203.18
        assert plane.longitude == 10.0
        assert plane.latitude == 20.0
        assert plane.icao24 == "abc123"
        assert plane.on_ground is False
        assert plane.current_country == "France"

    def test_aeroplane_init_with_none_values(self) -> None:
        """Проверяет инициализацию с None значениями."""
        plane = Aeroplane(
            callsign="TEST",
            origin_country="Test",
            velocity=None,
            baro_altitude=None,
        )

        assert plane.velocity == 0.0
        assert plane.baro_altitude == 0.0
        assert plane.longitude is None
        assert plane.latitude is None
        assert plane.icao24 == "Неизвестно"
        assert plane.on_ground is False
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

    def test_altitude_setter(self) -> None:
        """Проверяет сеттер для высоты."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        plane.baro_altitude = 15000
        assert plane.baro_altitude == 15000

        plane.baro_altitude = -50
        assert plane.baro_altitude == 0.0

    def test_callsign_setter(self) -> None:
        """Проверяет сеттер для позывного."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        plane.callsign = "NEW123"
        assert plane.callsign == "NEW123"

    def test_callsign_setter_empty(self) -> None:
        """Проверяет, что пустой позывной вызывает ошибку."""
        plane = Aeroplane("TEST", "Test", 100, 10000)

        with pytest.raises(ValueError, match="Позывной/наименование не может быть пустым"):
            plane.callsign = ""

        with pytest.raises(ValueError, match="Позывной/наименование не может быть пустым"):
            plane.callsign = "   "

    def test_origin_country_setter(self) -> None:
        """Проверяет сеттер для страны регистрации."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        plane.origin_country = "France"
        assert plane.origin_country == "France"

    def test_origin_country_setter_empty(self) -> None:
        """Проверяет, что пустая страна вызывает ошибку."""
        plane = Aeroplane("TEST", "Test", 100, 10000)

        with pytest.raises(ValueError, match="Страна регистрации не может быть пустой"):
            plane.origin_country = ""

        with pytest.raises(ValueError, match="Страна регистрации не может быть пустой"):
            plane.origin_country = "   "

    def test_current_country_setter(self) -> None:
        """Проверяет сеттер для текущей страны."""
        plane = Aeroplane("TEST", "Test", 100, 10000)
        plane.current_country = "Germany"
        assert plane.current_country == "Germany"

    def test_comparison_by_velocity(self) -> None:
        """Проверяет сравнение по скорости."""
        plane1 = Aeroplane("A", "US", 100, 10000)
        plane2 = Aeroplane("B", "US", 200, 10000)

        assert plane1 < plane2
        assert plane2 > plane1
        assert plane1 <= plane2
        assert plane2 >= plane1

    def test_comparison_by_velocity_equal(self) -> None:
        """Проверяет сравнение по скорости при равенстве."""
        plane1 = Aeroplane("A", "US", 100, 10000)
        plane2 = Aeroplane("B", "US", 100, 20000)

        assert not (plane1 < plane2)
        assert not (plane1 > plane2)
        assert plane1 <= plane2
        assert plane1 >= plane2

    def test_compare_altitude(self) -> None:
        """Проверяет сравнение по высоте."""
        plane1 = Aeroplane("A", "US", 100, 5000)
        plane2 = Aeroplane("B", "US", 200, 10000)

        assert plane1.compare_altitude(plane2) == -1
        assert plane2.compare_altitude(plane1) == 1

        plane3 = Aeroplane("C", "US", 150, 5000)
        assert plane1.compare_altitude(plane3) == 0

    def test_compare_altitude_with_invalid_type(self) -> None:
        """Проверяет, что сравнение с не-Aeroplane вызывает ошибку."""
        plane = Aeroplane("A", "US", 100, 5000)

        with pytest.raises(TypeError, match="Можно сравнивать только объекты Aeroplane"):
            plane.compare_altitude("not a plane")  # type: ignore

    def test_equality_with_invalid_type(self) -> None:
        """Проверяет сравнение с объектом не Aeroplane."""
        plane = Aeroplane("A", "US", 100, 10000)

        assert (plane == "not a plane") is False
        assert (plane != "not a plane") is True

    def test_from_dict(self) -> None:
        """Проверяет создание объекта из словаря."""
        data = {
            "callsign": "SWR123",
            "origin_country": "Switzerland",
            "velocity": 280.5,
            "baro_altitude": 11000.0,
            "longitude": 8.5,
            "latitude": 47.0,
            "icao24": "swiss123",
            "on_ground": False,
            "current_country": "Italy",
        }

        plane = Aeroplane.from_dict(data)

        assert plane.callsign == "SWR123"
        assert plane.origin_country == "Switzerland"
        assert plane.velocity == 280.5
        assert plane.baro_altitude == 11000.0
        assert plane.longitude == 8.5
        assert plane.latitude == 47.0
        assert plane.icao24 == "swiss123"
        assert plane.on_ground is False
        assert plane.current_country == "Italy"

    def test_from_dict_missing_fields(self) -> None:
        """Проверяет создание объекта из словаря с отсутствующими полями."""
        data = {
            "callsign": "SWR123",
            "origin_country": "Switzerland",
        }

        plane = Aeroplane.from_dict(data)

        assert plane.callsign == "SWR123"
        assert plane.origin_country == "Switzerland"
        assert plane.velocity == 0.0
        assert plane.baro_altitude == 0.0
        assert plane.longitude is None
        assert plane.latitude is None
        assert plane.icao24 == "Неизвестно"
        assert plane.on_ground is False
        assert plane.current_country == "Неизвестно"

    def test_to_dict(self) -> None:
        """Проверяет преобразование объекта в словарь."""
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

        data = plane.to_dict()

        assert data["callsign"] == "UAL1621"
        assert data["origin_country"] == "United States"
        assert data["velocity"] == 268.79
        assert data["baro_altitude"] == 10203.18
        assert data["longitude"] == 10.0
        assert data["latitude"] == 20.0
        assert data["icao24"] == "abc123"
        assert data["on_ground"] is False
        assert data["current_country"] == "France"

    def test_cast_to_object_list(self) -> None:
        """Проверяет преобразование списка словарей в список объектов."""
        data_list = [
            {"callsign": "A", "origin_country": "US", "velocity": 100, "baro_altitude": 10000},
            {"callsign": "B", "origin_country": "UK", "velocity": 200, "baro_altitude": 20000},
        ]

        planes = Aeroplane.cast_to_object_list(data_list, "France")

        assert len(planes) == 2
        assert planes[0].callsign == "A"
        assert planes[0].current_country == "France"
        assert planes[1].callsign == "B"
        assert planes[1].current_country == "France"

    def test_cast_to_object_list_empty(self) -> None:
        """Проверяет преобразование пустого списка."""
        planes = Aeroplane.cast_to_object_list([], "France")
        assert planes == []

    def test_str(self) -> None:
        """Проверяет строковое представление."""
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

        result = str(plane)

        assert "UAL1621" in result
        assert "United States" in result
        assert "France" in result
        assert "268.8" in result
        assert "10203.2" in result
        assert "abc123" in result
        assert "20.0" in result
        assert "10.0" in result
        assert "Нет" in result

    def test_repr(self) -> None:
        """Проверяет repr представление."""
        plane = Aeroplane(
            callsign="UAL1621",
            origin_country="United States",
            velocity=268.79,
            baro_altitude=10203.18,
            current_country="France",
        )

        result = repr(plane)

        assert "UAL1621" in result
        assert "United States" in result
        assert "France" in result
        assert "268.79" in result
        assert "10203.18" in result