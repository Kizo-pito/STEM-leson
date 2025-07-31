import google.generativeai as genai

API_KEY = "AIzaSyBld67u3T-_DKfoyLh3WYrr4N2YRGpGYCo"
genai.configure(api_key=API_KEY)

# Dùng model mới
model = genai.GenerativeModel("gemini-1.5-flash-latest")

response = model.generate_content("Tạo nội dung bài giảng về nguồn gốc Trái Đất")
print(response.text)
