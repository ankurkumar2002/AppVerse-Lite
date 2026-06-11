import requests

def fetch_apps_by_category(category):
    url = f"http://app-service:8082/api/apps/internal/apps/category/{category}"

    headers = {
        "X-INTERNAL-KEY": "my-secret-key"
    }

    response = requests.get(url, headers=headers, timeout=10)

    print("SPRING STATUS:", response.status_code)
    print("SPRING BODY:", response.text)

    response.raise_for_status()
    return response.json()
