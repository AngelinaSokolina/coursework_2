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


def filter_by_origin_country(aeroplanes: list[Aeroplane], countries_str: str) -> list[Aeroplane]:
    """
    Фильтрует самолеты по стране регистрации.

    Args:
        aeroplanes: Список самолетов
        countries_str: Строка со странами через запятую

    Returns:
        list[Aeroplane]: Отфильтрованный список
    """
    if not countries_str or not countries_str.strip():
        return aeroplanes

    # Разбиваем строку на список стран
    countries = [c.strip().lower() for c in countries_str.split(',') if c.strip()]

    if not countries:
        return aeroplanes

    filtered = []
    for plane in aeroplanes:
        if plane.origin_country.lower() in countries:
            filtered.append(plane)

    return filtered


def print_aeroplanes(aeroplanes: list[Aeroplane], title: str = "Топ самолетов") -> None:
    """Выводит информацию о самолетах в консоль."""
    if not aeroplanes:
        print("Самолетов не найдено")
        return

    print(f"\n{'=' * 70}")
    print(f"{title} ({len(aeroplanes)} шт.)")
    print('=' * 70)

    for i, plane in enumerate(aeroplanes, 1):
        print(f"{i}. {plane}")
        print("-" * 50)


def delete_menu(storage: JSONStorage) -> None:
    """
    Меню для удаления самолетов из файла.
    """
    print("\n" + "=" * 50)
    print("Управление данными в файле")
    print("=" * 50)

    count = storage.count()
    print(f"В файле находится {count} записей о самолетах.")

    if count == 0:
        print("Файл пуст. Удалять нечего.")
        return

    while True:
        print("\nВыберите действие:")
        print("1. Удалить самолеты по стране регистрации")
        print("2. Удалить самолеты с высотой ниже указанной")
        print("3. Удалить самолет по позывному")
        print("4. Показать все сохраненные самолеты")
        print("5. Очистить файл полностью")
        print("6. Выйти из меню удаления")

        choice = input("\nВведите номер действия: ").strip()

        if choice == "1":
            country = input("Введите страну регистрации для удаления: ").strip()
            if not country:
                print("Ошибка: страна не может быть пустой")
                continue

            planes_to_delete = storage.get_aeroplanes(origin_country=country)
            if not planes_to_delete:
                print(f"Самолетов с регистрацией в '{country}' не найдено")
                continue

            print(f"Найдено {len(planes_to_delete)} самолетов с регистрацией в '{country}'.")
            confirm = input(f"Удалить все {len(planes_to_delete)} самолетов? (да/нет): ").strip().lower()
            if confirm in ("да", "yes", "y"):
                storage.delete_by_criteria(origin_country=country)
                print(f"Удалено {len(planes_to_delete)} самолетов с регистрацией в '{country}'")
            else:
                print("Удаление отменено")

        elif choice == "2":
            try:
                altitude = float(input("Введите минимальную высоту (м): ").strip())
                if altitude < 0:
                    print("Ошибка: высота не может быть отрицательной")
                    continue

                planes_to_delete = storage.get_aeroplanes()
                to_delete = [p for p in planes_to_delete if p.baro_altitude < altitude]

                if not to_delete:
                    print(f"Самолетов с высотой ниже {altitude} м не найдено")
                    continue

                print(f"Найдено {len(to_delete)} самолетов с высотой ниже {altitude} м.")
                confirm = input(f"Удалить все {len(to_delete)} самолетов? (да/нет): ").strip().lower()
                if confirm in ("да", "yes", "y"):
                    for plane in to_delete:
                        storage.delete_aeroplane(plane)
                    print(f"Удалено {len(to_delete)} самолетов с высотой ниже {altitude} м")
                else:
                    print("Удаление отменено")

            except ValueError:
                print("Ошибка: введите число")

        elif choice == "3":
            callsign = input("Введите позывной/наименование самолета для удаления: ").strip().upper()
            if not callsign:
                print("Ошибка: позывной/наименование не может быть пустым")
                continue

            planes = storage.get_aeroplanes()
            to_delete = [p for p in planes if p.callsign.upper() == callsign]

            if not to_delete:
                print(f"Самолет с позывным/наименованием '{callsign}' не найден")
                continue

            print(f"Найден самолет с позывным/наименованием '{callsign}':")
            print(to_delete[0])
            confirm = input(f"Удалить этот самолет? (да/нет): ").strip().lower()
            if confirm in ("да", "yes", "y"):
                storage.delete_aeroplane(to_delete[0])
                print(f"Самолет '{callsign}' удален")
            else:
                print("Удаление отменено")

        elif choice == "4":
            all_planes = storage.get_all()
            if not all_planes:
                print("Файл пуст")
            else:
                print_aeroplanes(all_planes, "Все сохраненные самолеты")

        elif choice == "5":
            confirm = input("Вы уверены, что хотите очистить весь файл? (да/нет): ").strip().lower()
            if confirm in ("да", "yes", "y"):
                storage.clear()
                print("Файл полностью очищен")
            else:
                print("Очистка отменена")

        elif choice == "6":
            print("Выход из меню удаления.")
            break

        else:
            print("Ошибка: неверный выбор. Попробуйте снова.")

        count = storage.count()
        print(f"\nВ файле осталось {count} записей.")


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль."""
    print("Добро пожаловать в систему отслеживания самолетов!")
    print("=" * 50)

    api = APIAdapter()
    json_saver = JSONStorage()

    # Всегда очищаем файл при новом запуске
    json_saver.clear()
    print("Файл data/aeroplanes.json очищен для новых данных.")

    # ===== БЕСКОНЕЧНЫЙ ЦИКЛ ВВОДА СТРАНЫ =====
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

        # Проверяем, существует ли страна в API
        try:
            print(f"\nПроверка страны '{country}'...")
            coords = api.get_country_coordinates(country)
            print(f"Страна '{country}' найдена! Координаты получены.")
            break  # Выходим из цикла, если страна найдена

        except ValueError:
            print(f"Ошибка: страна '{country}' не найдена. Проверьте правильность написания и попробуйте снова.")
            continue
        except ConnectionError as e:
            print(f"Ошибка подключения к API: {e}")
            print("Попробуйте позже или проверьте интернет-соединение.")
            return

    # ===== Получение данных о самолетах =====
    try:
        print(f"\nПоиск самолетов в воздушном пространстве '{country}'...")

        data = api.get_aeroplanes(country)

        if not data:
            print(f"Самолетов в воздушном пространстве '{country}' не найдено")
            return

        aeroplanes = Aeroplane.cast_to_object_list(data, country)
        print(f"Найдено самолетов: {len(aeroplanes)}")

        # ===== Ввод количества для топа =====
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

        # ===== СОРТИРОВКА И ТОП =====
        sorted_aeroplanes = sort_aeroplanes(aeroplanes)
        top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)

        # Сохраняем в файл
        for plane in top_aeroplanes:
            json_saver.add_aeroplane(plane)

        print(f"\nСохранено {len(top_aeroplanes)} самолетов в файл data/aeroplanes.json")

        print_aeroplanes(top_aeroplanes, f"Топ {len(top_aeroplanes)} самолетов по высоте")

        # ===== ДОПОЛНИТЕЛЬНАЯ ФИЛЬТРАЦИЯ =====
        # Фильтрация по стране регистрации (как требуется в задании)
        filter_country = input("\nХотите отфильтровать самолеты по стране регистрации? (да/нет): ").strip().lower()
        if filter_country in ("да", "yes", "y"):
            countries_str = input("Введите страны через запятую (например, United States, France): ").strip()
            filtered_planes = filter_by_origin_country(aeroplanes, countries_str)
            if filtered_planes:
                print_aeroplanes(filtered_planes, "Отфильтрованные по стране регистрации")
            else:
                print("Самолеты с указанными странами регистрации не найдены.")

        # ===== Меню удаления =====
        delete_menu(json_saver)

    except (ConnectionError, RuntimeError) as e:
        print(f"Ошибка при получении данных: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    user_interaction()