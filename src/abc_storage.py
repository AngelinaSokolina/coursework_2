from abc import ABC, abstractmethod
from typing import Any


class ABCStorage(ABC):
    """
    Абстрактный класс для работы с хранилищем данных о самолетах.
    Определяет интерфейс для добавления, получения и удаления данных.
    Данный класс выступает в роли основы для коннектора,
    заменяя который можно использовать различные хранилища (БД, удаленное хранилище и т.д.).
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane: Any) -> None:  # pragma: no cover
        """
        Добавляет информацию о самолете в хранилище.

        Args:
            aeroplane (Any): Объект самолета для добавления
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria: Any) -> list[Any]:  # pragma: no cover
        """
        Получает данные о самолетах по указанным критериям.

        Args:
            **criteria: Критерии фильтрации (например, origin_country="United States")

        Returns:
            list[Any]: Список объектов самолетов, соответствующих критериям
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Any) -> None:  # pragma: no cover
        """
        Удаляет информацию о самолете из хранилища.

        Args:
            aeroplane (Any): Объект самолета для удаления
        """
        pass

    @abstractmethod
    def delete_by_criteria(self, **criteria: Any) -> None:  # pragma: no cover
        """
        Удаляет информацию о самолетах по указанным критериям.

        Args:
            **criteria: Критерии для удаления (например, origin_country="United States")
        """
        pass

    @abstractmethod
    def clear(self) -> None:  # pragma: no cover
        """Полностью очищает хранилище."""
        pass

    @abstractmethod
    def get_all(self) -> list[Any]:  # pragma: no cover
        """
        Получает все данные из хранилища.

        Returns:
            list[Any]: Список всех объектов в хранилище
        """
        pass

    @abstractmethod
    def count(self) -> int:  # pragma: no cover
        """
        Возвращает количество записей в хранилище.

        Returns:
            int: Количество записей
        """
        pass
