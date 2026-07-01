import os
import tempfile

import pytest

from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


class TestJSONStorage:
    """Тесты для класса JSONStorage."""

    def test_add_and_get_aeroplane(self) -> None:
        """Проверяет добавление и получение самолета."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp.close()  # ← закрываем файл!
            storage = JSONStorage(tmp.name)

            plane = Aeroplane(
                callsign="UAL1621",
                origin_country="United States",
                velocity=268.79,
                baro_altitude=10203.18,
                icao24="abc123",
            )

            storage.add_aeroplane(plane)
            planes = storage.get_aeroplanes()

            assert len(planes) == 1
            assert planes[0].callsign == "UAL1621"
            assert planes[0].icao24 == "abc123"

            os.unlink(tmp.name)

    def test_update_existing_aeroplane(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp.close()
            storage = JSONStorage(tmp.name)

            plane1 = Aeroplane(
                callsign="UAL1621",
                origin_country="United States",
                velocity=268.79,
                baro_altitude=10203.18,
                icao24="abc123",
            )

            plane2 = Aeroplane(
                callsign="UAL1621",
                origin_country="United States",
                velocity=300.0,
                baro_altitude=11000.0,
                icao24="abc123",
            )

            storage.add_aeroplane(plane1)
            storage.add_aeroplane(plane2)

            planes = storage.get_aeroplanes()
            assert len(planes) == 1
            assert planes[0].velocity == 300.0

            os.unlink(tmp.name)

    def test_get_aeroplanes_by_criteria(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp.close()
            storage = JSONStorage(tmp.name)

            plane1 = Aeroplane(
                callsign="UAL1621",
                origin_country="United States",
                velocity=268.79,
                baro_altitude=10203.18,
                icao24="abc123",
            )

            plane2 = Aeroplane(
                callsign="AFR123",
                origin_country="France",
                velocity=250.0,
                baro_altitude=9500.0,
                icao24="def456",
            )

            storage.add_aeroplane(plane1)
            storage.add_aeroplane(plane2)

            planes = storage.get_aeroplanes(origin_country="United States")
            assert len(planes) == 1
            assert planes[0].callsign == "UAL1621"

            os.unlink(tmp.name)

    def test_delete_aeroplane(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp.close()
            storage = JSONStorage(tmp.name)

            plane = Aeroplane(
                callsign="UAL1621",
                origin_country="United States",
                velocity=268.79,
                baro_altitude=10203.18,
                icao24="abc123",
            )

            storage.add_aeroplane(plane)
            assert storage.count() == 1

            storage.delete_aeroplane(plane)
            assert storage.count() == 0

            os.unlink(tmp.name)

    def test_delete_by_criteria(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp.close()
            storage = JSONStorage(tmp.name)

            plane1 = Aeroplane(
                callsign="UAL1621",
                origin_country="United States",
                velocity=268.79,
                baro_altitude=10203.18,
                icao24="abc123",
            )

            plane2 = Aeroplane(
                callsign="AFR123",
                origin_country="France",
                velocity=250.0,
                baro_altitude=9500.0,
                icao24="def456",
            )

            storage.add_aeroplane(plane1)
            storage.add_aeroplane(plane2)

            storage.delete_by_criteria(origin_country="United States")
            planes = storage.get_aeroplanes()

            assert len(planes) == 1
            assert planes[0].callsign == "AFR123"

            os.unlink(tmp.name)

    def test_clear(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp.close()
            storage = JSONStorage(tmp.name)

            plane = Aeroplane(
                callsign="UAL1621",
                origin_country="United States",
                velocity=268.79,
                baro_altitude=10203.18,
                icao24="abc123",
            )
            storage.add_aeroplane(plane)
            assert storage.count() == 1

            storage.clear()
            assert storage.count() == 0

            os.unlink(tmp.name)

    def test_load_data_with_corrupted_file(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp.close()
            with open(tmp.name, "w", encoding="utf-8") as f:
                f.write("{некорректный json}")

            storage = JSONStorage(tmp.name)
            assert storage.get_aeroplanes() == []

            os.unlink(tmp.name)
