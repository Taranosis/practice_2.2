import requests

try:
    github_user = input("Введите имя пользователя GitHub: ").strip()
    if not github_user:
        print("Ошибка: имя пользователя не может быть пустым.")
        exit()

    profile_url = f"https://api.github.com/users/{github_user}"
    profile_resp = requests.get(profile_url)

    if profile_resp.status_code == 404:
        print("Ошибка: пользователь не найден.")
        exit()
    if profile_resp.status_code != 200:
        print("Ошибка: не удалось получить данные профиля.")
        exit()

    profile_data = profile_resp.json()

    print("\n--- Профиль пользователя ---")
    print("Имя:", profile_data.get("name"))
    print("Ссылка:", profile_data.get("html_url"))
    print("Количество репозиториев:", profile_data.get("public_repos"))
    print("Количество подписок:", profile_data.get("following"))
    print("Количество подписчиков:", profile_data.get("followers"))

    repos_url = profile_url + "/repos"
    repos_resp = requests.get(repos_url)
    if repos_resp.status_code != 200:
        print("Ошибка: не удалось получить список репозиториев.")
        exit()

    repos_list = repos_resp.json()
    print("\n--- Репозитории ---")
    if not repos_list:
        print("У пользователя нет репозиториев.")
    else:
        for repo in repos_list:
            print("Название:", repo.get("name"))
            print("Ссылка:", repo.get("html_url"))
            print("Язык:", repo.get("language"))
            print("Видимость:", repo.get("visibility") or "public")
            print("Ветка по умолчанию:", repo.get("default_branch"))
            print("-" * 30)

    search_query = input("\nВведите название репозитория для поиска: ").strip()
    if search_query:
        search_resp = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": search_query}
        )
        if search_resp.status_code == 200:
            search_results = search_resp.json().get("items", [])
            print(f"\n--- Результаты поиска для '{search_query}' ---")
            if not search_results:
                print("Репозитории не найдены.")
            else:
                for repo in search_results:
                    print("Название:", repo.get("name"))
                    print("Ссылка:", repo.get("html_url"))
                    print("Описание:", repo.get("description"))
                    print("-" * 30)
        else:
            print("Ошибка: не удалось выполнить поиск репозиториев.")

except Exception:
    print("Произошла ошибка.")