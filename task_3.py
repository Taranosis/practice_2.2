import json
import requests
import os

API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = "resource/save.json"

def read():
    if not os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_rates():
    try:
        r = requests.get(API_URL, timeout=5)
        r.raise_for_status()
        return r.json().get("Valute", {})
    except requests.RequestException as e:
        print(f"Ошибка получения данных: {e}")
        return {}

def main():
    data = read()
    rates = get_rates()

    while True:
        print("\n1 - Показать все курсы  2 - Показать курс одной валюты  3 - Создать группу")
        print("4 - Список групп  5 - Добавить валюту в группу  6 - Удалить валюту из группы  0 - Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            for code, val in rates.items():
                print(f"{code}: {val['Value']}")
        elif choice == "2":
            code = input("Введите код валюты: ").upper()
            value = rates.get(code, {}).get('Value')
            if value is not None:
                print(f"{code}: {value}")
            else:
                print("Валюта не найдена")
        elif choice == "3":
            name = input("Имя группы: ").strip()
            if not name:
                print("Имя группы не может быть пустым")
                continue
            if name not in data:
                data[name] = []
            while True:
                code = input("Введите код валюты (Enter — выход): ").upper()
                if not code:
                    break
                if code in rates:
                    if code not in data[name]:
                        data[name].append(code)
                        print("Добавлено")
                    else:
                        print("Эта валюта уже в группе")
                else:
                    print("Валюта не найдена")
            save(data)
            print("Группа сохранена")
        elif choice == "4":
            if not data:
                print("Нет групп")
            else:
                for n, vals in data.items():
                    print(f"{n}: {vals}")
        elif choice == "5":
            name = input("Группа: ").strip()
            code = input("Код валюты: ").upper()
            if name in data and code in rates:
                if code not in data[name]:
                    data[name].append(code)
                    save(data)
                    print("Добавлено")
                else:
                    print("В группе уже есть эта валюта")
            else:
                print("Ошибка: группа или валюта не найдены")
        elif choice == "6":
            name = input("Группа: ").strip()
            code = input("Код валюты: ").upper()
            if name in data and code in data[name]:
                data[name].remove(code)
                save(data)
                print("Удалено")
            else:
                print("Ошибка: группа или валюта не найдены")
        elif choice == "0":
            save(data)
            print("Данные сохранены. Выход.")
            break
        else:
            print("Неверный ввод, попробуйте снова")

if __name__ == "__main__":
    main()