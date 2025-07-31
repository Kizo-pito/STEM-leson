import requests

url = "http://127.0.0.1:5000/generate-lesson"
payload = {"prompt": "Tạo bài giảng môn Khoa học lớp 6 về năng lượng"}

response = requests.post(url, json=payload)

print("Raw response text:")
print(response.text)  # 👈 Thêm dòng này

print("Kết quả nhận được từ AI:")
print(response.json())
