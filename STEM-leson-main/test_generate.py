import requests

BASE_URL = "http://127.0.0.1:5000"  # hoặc localhost:5000 nếu dùng cục bộ

def get_jwt_token():
    login_data = {
        "username": "testuser",         # <--- phải là user đã được đăng ký
        "password": "testpassword"
    }
    res = requests.post(f"{BASE_URL}/login", json=login_data)
    print("Login response:", res.status_code, res.text)
    return res.json().get("access_token")

def test_create_lesson():
    token = get_jwt_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "grade": "5",
        "subject": "Khoa học",
        "topic": "Hệ mặt trời",
        "requests": "Có ví dụ minh hoạ"
    }

    res = requests.post(f"{BASE_URL}/api/generate/lesson", json=data, headers=headers)
    print("Response:", res.status_code)
    print(res.json())

test_create_lesson()
