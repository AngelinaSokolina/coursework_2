import pytest
from unittest.mock import Mock, patch
from typing import Any

from src.api import APIAdapter
from src.abc_api import ABCAPI


# ====================== Для абстрактного класса ABCAPI =================================

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

    def test_abstract_methods_have_docstrings(self) -> None:
        """Проверяет, что все абстрактные методы имеют документацию."""
        methods = [
            ABCAPI.get_country_coordinates,
            ABCAPI.get_aeroplanes,
            ABCAPI.get_aeroplanes_by_bounding_box,
        ]

        for method in methods:
            assert method.__doc__ is not None
            assert len(method.__doc__.strip()) > 0

    def test_abstract_methods_have_correct_annotations(self) -> None:
        """Проверяет, что методы имеют правильные аннотации типов."""
        sig = ABCAPI.get_country_coordinates.__annotations__
        assert "return" in sig
        assert sig["return"] == list[float]

        sig = ABCAPI.get_aeroplanes.__annotations__
        assert "return" in sig
        assert sig["return"] == list[dict[str, Any]]

        sig = ABCAPI.get_aeroplanes_by_bounding_box.__annotations__
        assert "return" in sig
        assert sig["return"] == list[dict[str, Any]]


# ====================== Для абстрактного класса ABCStorage =================================

class TestABCStorage:

    def test_abc_storage_is_abstract(self) -> None:
        """Проверяет, что ABCStorage является абстрактным классом."""
        from src.abc_storage import ABCStorage

        import abc
        assert ABCStorage is not None
        assert isinstance(ABCStorage, abc.ABCMeta)

    def test_abc_storage_cannot_be_instantiated(self) -> None:
        """Проверяет, что нельзя создать экземпляр абстрактного класса."""
        from src.abc_storage import ABCStorage

        with pytest.raises(TypeError) as exc_info:
            ABCStorage()  # type: ignore

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_abc_storage_has_abstract_methods(self) -> None:
        """Проверяет, что все абстрактные методы объявлены."""
        from src.abc_storage import ABCStorage

        abstract_methods = ABCStorage.__abstractmethods__

        assert "add_aeroplane" in abstract_methods
        assert "get_aeroplanes" in abstract_methods
        assert "delete_aeroplane" in abstract_methods
        assert "delete_by_criteria" in abstract_methods
        assert "clear" in abstract_methods
        assert "get_all" in abstract_methods
        assert "count" in abstract_methods


# ====================== Для класса APIAdapter (только моки) =================================

class TestAPIAdapter:

    def test_api_adapter_init(self) -> None:
        """Проверяет инициализацию APIAdapter."""
        api = APIAdapter()

        assert api.openstreetmap_url == "https://nominatim.openstreetmap.org/search"
        assert api.opensky_url == "https://opensky-network.org/api/states/all"
        assert api.timeout == 15
        assert api.user_agent == "coursework-app/1.0"
        assert api.aeroplanes == []

    @patch("src.api.requests.get")
    def test_get_country_coordinates_success(self, mock_get: Mock) -> None:
        """Проверяет успешное получение координат страны."""
        api = APIAdapter()

        mock_response = Mock()
        mock_response.json.return_value = [
            {"boundingbox": ["36.0", "44.0", "-10.0", "4.0"]}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        coords = api.get_country_coordinates("Spain")

        assert coords == [36.0, 44.0, -10.0, 4.0]
        mock_get.assert_called_once()

    @patch("src.api.requests.get")
    def test_get_country_coordinates_empty_country(self, mock_get: Mock) -> None:
        """Проверяет, что при пустом названии страны выбрасывается ошибка."""
        api = APIAdapter()

        with pytest.raises(ValueError, match="Название страны не может быть пустым"):
            api.get_country_coordinates("")

        mock_get.assert_not_called()

    @patch("src.api.requests.get")
    def test_get_country_coordinates_not_found(self, mock_get: Mock) -> None:
        """Проверяет, что при несуществующей стране выбрасывается ошибка."""
        api = APIAdapter()

        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Страна 'Nonexistent' не найдена"):
            api.get_country_coordinates("Nonexistent")

    @patch("src.api.requests.get")
    def test_get_aeroplanes_success(self, mock_get: Mock) -> None:
        """Проверяет успешное получение самолетов."""
        api = APIAdapter()

        mock_response_coords = Mock()
        mock_response_coords.json.return_value = [
            {"boundingbox": ["36.0", "44.0", "-10.0", "4.0"]}
        ]
        mock_response_coords.raise_for_status.return_value = None

        mock_response_planes = Mock()
        mock_response_planes.json.return_value = {
            "states": [
                ["abc123", "TEST123", "United States", None, None, 10.0, 20.0, 10000.0, False, 250.0, None, None, None, None, None, None, None]
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
    def test_get_aeroplanes_empty_country(self, mock_get: Mock) -> None:
        """Проверяет, что при пустом названии страны выбрасывается ошибка."""
        api = APIAdapter()

        with pytest.raises(ValueError, match="Название страны не может быть пустым"):
            api.get_aeroplanes("")

        mock_get.assert_not_called()

    @patch("src.api.requests.get")
    def test_get_aeroplanes_country_not_found(self, mock_get: Mock) -> None:
        """Проверяет, что при несуществующей стране выбрасывается ошибка."""
        api = APIAdapter()

        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Страна 'Nonexistent' не найдена"):
            api.get_aeroplanes("Nonexistent")

    @patch("src.api.requests.get")
    def test_get_aeroplanes_by_bounding_box_success(self, mock_get: Mock) -> None:
        """Проверяет получение самолетов по bounding box."""
        api = APIAdapter()

        mock_response = Mock()
        mock_response.json.return_value = {
            "states": [
                ["abc123", "TEST456", "France", None, None, 5.0, 45.0, 11000.0, False, 300.0, None, None, None, None, None, None, None]
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
        mock_response.json.return_value = {"states": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        bbox = [36.0, 44.0, -10.0, 4.0]
        data = api.get_aeroplanes_by_bounding_box(bbox)

        assert data == []

    def test_get_aeroplanes_by_bounding_box_invalid(self) -> None:
        """Проверяет, что при некорректном bbox выбрасывается ошибка."""
        api = APIAdapter()

        with pytest.raises(ValueError, match="Некорректный bounding box"):
            api.get_aeroplanes_by_bounding_box([])

        with pytest.raises(ValueError, match="Некорректный bounding box"):
            api.get_aeroplanes_by_bounding_box([1.0, 2.0, 3.0])

        with pytest.raises(ValueError, match="Все координаты должны быть числами"):
            api.get_aeroplanes_by_bounding_box(["a", "b", "c", "d"])  # type: ignore

    def test_parse_states(self) -> None:
        """Проверяет парсинг данных от opensky."""
        api = APIAdapter()

        test_states = [
            [
                "abc123", "TEST123", "United States", 1234567890, 1234567890,
                10.0, 20.0, 10000.0, False, 250.0, 90.0, 0.0,
                None, 10100.0, "1234", False, 0
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
        """Проверяет парсинг неполных данных."""
        api = APIAdapter()
        test_states = [["abc123", "TEST123"]]
        result = api._parse_states(test_states)
        assert result == []

    def test_parse_states_with_none_values(self) -> None:
        """Проверяет парсинг данных с None значениями."""
        api = APIAdapter()

        test_states = [
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        ]

        result = api._parse_states(test_states)

        assert len(result) == 1
        assert result[0]["icao24"] == "Неизвестно"
        assert result[0]["callsign"] == "Неизвестно"
        assert result[0]["origin_country"] == "Неизвестно"
        assert result[0]["on_ground"] is False

    @patch("src.api.requests.get")
    def test_connection_error_handling(self, mock_get: Mock) -> None:
        """Проверяет обработку ошибок подключения."""
        import requests
        api = APIAdapter()

        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        with pytest.raises(ConnectionError, match="Ошибка при запросе к nominatim API"):
            api.get_country_coordinates("Spain")