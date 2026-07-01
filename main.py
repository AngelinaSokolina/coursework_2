from src.api import APIAdapter
from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage

MAX_TOP = 15


def validate_country(country: str) -> str | None:
    """
    Проверяет корректность ввода названия страны на английском.
    """
    if not country or not country.strip():
        return None

    country = country.strip()

    if not all(c.isalpha() or c.isspace() for c in country):
        print("Ошибка: название страны должно содержать только буквы")
        return None

    return country.title()


def sort_aeroplanes(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортирует самолеты по высоте (по убыванию)."""
    return sorted(aeroplanes, key=lambda p: p.baro_altitude, reverse=True)


def get_top_aeroplanes(aeroplanes: list[Aeroplane], top_n: int) -> list[Aeroplane]:
    """Возвращает топ N самолетов (не больше MAX_TOP)."""
    if top_n <= 0:
        return []
    if top_n > MAX_TOP:
        print(f"Предупреждение: максимальное количество — {MAX_TOP}. Берём {MAX_TOP}.")
        top_n = MAX_TOP
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Выводит информацию о самолетах в консоль."""
    if not aeroplanes:
        print("Самолетов не найдено")
        return

    print(f"\n{'=' * 70}")
    print(f"Топ {len(aeroplanes)} самолетов по высоте")
    print('=' * 70)

    for i, plane in enumerate(aeroplanes, 1):
        print(f"{i}. {plane}")
        print("-" * 50)


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль."""
    print("Добро пожаловать в систему отслеживания самолетов!")
    print("=" * 50)

    api = APIAdapter()

    while True:
        country = input("\nВведите название страны: ").strip()

        if not country:
            print("Ошибка: название страны не может быть пустым. Попробуйте снова.")
            continue

        validated_country = validate_country(country)

        if validated_country is None:
            print("Ошибка: некорректный ввод. Используйте только буквы. Попробуйте снова.")
            continue

        country = validated_country
        break

    try:
        print(f"\nПоиск самолетов в воздушном пространстве '{country}'...")

        try:
            data = api.get_aeroplanes(country)
        except ValueError as e:
            print(f"Ошибка: страна '{country}' не найдена. Проверьте правильность написания.")
            return
        except ConnectionError as e:
            print(f"Ошибка подключения к API: {e}")
            return

        if not data:
            print(f"Самолетов в воздушном пространстве '{country}' не найдено")
            return

        aeroplanes = Aeroplane.cast_to_object_list(data, country)
        print(f"Найдено самолетов: {len(aeroplanes)}")

        while True:
            try:
                top_n = input(f"\nВведите количество самолетов для вывода в топ N по высоте (до {MAX_TOP}): ").strip()

                if not top_n:
                    print("Ошибка: количество не может быть пустым. Попробуйте снова.")
                    continue

                top_n = int(top_n)

                if top_n <= 0:
                    print("Ошибка: количество должно быть положительным числом. Попробуйте снова.")
                    continue

                break

            except ValueError:
                print("Ошибка: введите целое положительное число. Попробуйте снова.")

        sorted_aeroplanes = sort_aeroplanes(aeroplanes)
        top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)

        json_saver = JSONStorage()
        json_saver.clear()
        for plane in top_aeroplanes:
            json_saver.add_aeroplane(plane)

        print(f"\nСохранено {len(top_aeroplanes)} самолетов в файл data/aeroplanes.json")

        print_aeroplanes(top_aeroplanes)

    except (ConnectionError, RuntimeError) as e:
        print(f"Ошибка при получении данных: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    user_interaction()