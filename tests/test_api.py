from src.api import APIAdapter

def test_api():
    print("=" * 50)
    print("Проверка работы API")
    print("=" * 50)

    api = APIAdapter()

    # 1. Проверка получения координат
    print("\n1. Получение координат Испании...")
    try:
        coords = api.get_country_coordinates("Spain")
        print(f"   ✅ Координаты получены: {coords}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # 2. Проверка получения самолетов
    print("\n2. Получение самолетов над Испанией...")
    try:
        data = api.get_aeroplanes("Spain")
        print(f"   ✅ Найдено самолетов: {len(data)}")
        if data:
            print(f"   ✅ Первый самолет: {data[0].get('callsign', 'Нет позывного')}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    print("\n" + "=" * 50)
    print("Проверка завершена!")


if __name__ == "__main__":
    test_api()