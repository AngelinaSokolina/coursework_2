from unittest.mock import Mock, patch

import pytest

from src.abc_api import ABCAPI
from src.abc_storage import ABCStorage
from src.api import APIAdapter

# ====================== ТЕСТЫ ДЛЯ АБСТРАКТНОГО КЛАССА ABCAPI =================================
# Эти тесты проверяют, что ABCAPI правильно объявлен как абстрактный класс


class TestABCAPI:

    def test_abc_api_is_abstract(self) -> None:
        """Проверяет, что ABCAPI является абстрактным классом"""
        import abc

        assert ABCAPI is not None
        assert isinstance(ABCAPI, abc.ABCMeta)

    def test_abc_api_cannot_be_instantiated(self) -> None:
        """Проверяет, что нельзя создать экземпляр абстрактного класса."""
        with pytest.raises(TypeError) as exc_info:
            ABCAPI()  # type: ignore

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_abc_api_has_abstract_methods(self) -> None:
        """Проверяет, что все абстрактные методы объявлены."""
        abstract_methods = ABCAPI.__abstractmethods__

        assert "get_country_coordinates" in abstract_methods
        assert "get_aeroplanes" in abstract_methods
        assert "get_aeroplanes_by_bounding_box" in abstract_methods


# ====================== ТЕСТЫ ДЛЯ АБСТРАКТНОГО КЛАССА ABCSTORAGE =================================
# Эти тесты проверяют, что ABCStorage правильно объявлен как абстрактный класс


class TestABCStorage:

    def test_abc_storage_is_abstract(self) -> None:
        """Проверяет, что ABCStorage является абстрактным классом."""
        import abc

        assert ABCStorage is not None
        assert isinstance(ABCStorage, abc.ABCMeta)

    def test_abc_storage_cannot_be_instantiated(self) -> None:
        """Проверяет, что нельзя создать экземпляр абстрактного класса."""
        with pytest.raises(TypeError) as exc_info:
            ABCStorage()  # type: ignore

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_abc_storage_has_abstract_methods(self) -> None:
        """Проверяет, что все абстрактные методы объявлены."""
        abstract_methods = ABCStorage.__abstractmethods__

        assert "add_aeroplane" in abstract_methods
        assert "get_aeroplanes" in abstract_methods
        assert "delete_aeroplane" in abstract_methods
        assert "delete_by_criteria" in abstract_methods
        assert "clear" in abstract_methods
        assert "get_all" in abstract_methods
        assert "count" in abstract_methods


# ====================== ТЕСТЫ ДЛЯ КЛАССА APIADAPTER =================================
# Эти тесты проверяют работу APIAdapter с реальными вызовами (через моки)


class TestAPIAdapter:

    def test_api_adapter_init(self) -> None:
        """Проверяет инициализацию APIAdapter."""
        api = APIAdapter()

        assert api.openstreetmap_url == "https://nominatim.openstreetmap.org/search"
        assert api.opensky_url == "https://opensky-network.org/api/states/all"
        assert api.timeout == 15
        assert api.aeroplanes == []

    @patch("src.api.requests.get")
    def test_get_country_coordinates_success(self, mock_get: Mock) -> None:
        """
        Проверяет успешное получение координат страны.
        Мокаем ответ API, чтобы он вернул координаты Испании.
        """
        api = APIAdapter()

        # Создаём поддельный ответ от API
        mock_response = Mock()
        mock_response.json.return_value = [{"boundingbox": ["36.0", "44.0", "-10.0", "4.0"]}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем метод
        coords = api.get_country_coordinates("Spain")

        # Проверяем результат
        assert coords == [36.0, 44.0, -10.0, 4.0]
        mock_get.assert_called_once()

    @patch("src.api.requests.get")
    def test_get_country_coordinates_empty_country(self, mock_get: Mock) -> None:
        """
        Проверяет, что при пустом названии страны выбрасывается ошибка.
        API не должно вызываться.
        """
        api = APIAdapter()

        with pytest.raises(ValueError, match="Название страны не может быть пустым"):
            api.get_country_coordinates("")

        mock_get.assert_not_called()

    @patch("src.api.requests.get")
    def test_get_country_coordinates_not_found(self, mock_get: Mock) -> None:
        """
        Проверяет, что при несуществующей стране выбрасывается ошибка.
        API возвращает пустой список.
        """
        api = APIAdapter()

        mock_response = Mock()
        mock_response.json.return_value = []  # ← страна не найдена
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Страна 'Nonexistent' не найдена"):
            api.get_country_coordinates("Nonexistent")

    @patch("src.api.requests.get")
    def test_get_aeroplanes_success(self, mock_get: Mock) -> None:
        """
        Проверяет успешное получение самолетов.
        Сначала мокаем получение координат страны, потом получение самолетов.
        """
        api = APIAdapter()

        # Мок для координат страны
        mock_response_coords = Mock()
        mock_response_coords.json.return_value = [{"boundingbox": ["36.0", "44.0", "-10.0", "4.0"]}]
        mock_response_coords.raise_for_status.return_value = None

        # Мок для самолетов
        mock_response_planes = Mock()
        mock_response_planes.json.return_value = {
            "states": [
                [
                    "abc123",
                    "TEST123",
                    "United States",
                    None,
                    None,
                    10.0,
                    20.0,
                    10000.0,
                    False,
                    250.0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ]
            ]
        }
        mock_response_planes.raise_for_status.return_value = None

        mock_get.side_effect = [mock_response_coords, mock_response_planes]

        data = api.get_aeroplanes("Spain")

        assert len(data) == 1
        assert data[0]["callsign"] == "TEST123"
        assert data[0]["origin_country"] == "United States"
        assert mock_get.call_count == 2

    @patch("src.api.requests.get")
    def test_get_aeroplanes_by_bounding_box_success(self, mock_get: Mock) -> None:
        """Проверяет получение самолетов по bounding box."""
        api = APIAdapter()

        mock_response = Mock()
        mock_response.json.return_value = {
            "states": [
                [
                    "abc123",
                    "TEST456",
                    "France",
                    None,
                    None,
                    5.0,
                    45.0,
                    11000.0,
                    False,
                    300.0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ]
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        bbox = [36.0, 44.0, -10.0, 4.0]
        data = api.get_aeroplanes_by_bounding_box(bbox)

        assert len(data) == 1
        assert data[0]["callsign"] == "TEST456"
        assert data[0]["origin_country"] == "France"
        mock_get.assert_called_once()

    @patch("src.api.requests.get")
    def test_get_aeroplanes_by_bounding_box_empty(self, mock_get: Mock) -> None:
        """Проверяет обработку пустого списка самолетов."""
        api = APIAdapter()

        mock_response = Mock()
        mock_response.json.return_value = {"states": []}  # ← пустой список
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        bbox = [36.0, 44.0, -10.0, 4.0]
        data = api.get_aeroplanes_by_bounding_box(bbox)

        assert data == []

    def test_parse_states(self) -> None:
        """Проверяет парсинг данных от opensky API."""
        api = APIAdapter()

        # Формат данных от opensky (индексы в массиве)
        test_states = [
            [
                "abc123",  # 0: icao24
                "TEST123",  # 1: callsign
                "United States",  # 2: origin_country
                None,
                None,  # 3-4: время
                10.0,
                20.0,  # 5-6: longitude, latitude
                10000.0,  # 7: baro_altitude
                False,  # 8: on_ground
                250.0,  # 9: velocity
                None,
                None,
                None,
                None,
                None,
                None,
                None,  # 10-16: остальные поля
            ]
        ]

        result = api._parse_states(test_states)

        assert len(result) == 1
        assert result[0]["icao24"] == "abc123"
        assert result[0]["callsign"] == "TEST123"
        assert result[0]["origin_country"] == "United States"
        assert result[0]["longitude"] == 10.0
        assert result[0]["latitude"] == 20.0
        assert result[0]["baro_altitude"] == 10000.0
        assert result[0]["velocity"] == 250.0
        assert result[0]["on_ground"] is False

    def test_parse_states_empty(self) -> None:
        """Проверяет парсинг пустого списка."""
        api = APIAdapter()
        result = api._parse_states([])
        assert result == []

    def test_parse_states_incomplete(self) -> None:
        """Проверяет парсинг неполных данных (пропускает)."""
        api = APIAdapter()
        test_states = [["abc123", "TEST123"]]  # ← неполные данные
        result = api._parse_states(test_states)
        assert result == []

    @patch("src.api.requests.get")
    def test_connection_error_handling(self, mock_get: Mock) -> None:
        """Проверяет обработку ошибок подключения к API."""
        import requests

        api = APIAdapter()

        # Мокаем ошибку подключения
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        with pytest.raises(ConnectionError, match="Ошибка при запросе к nominatim API"):
            api.get_country_coordinates("Spain")
