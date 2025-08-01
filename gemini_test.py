import google.generativeai as genai

API_KEY = "AIzaSyBCoxGcSbJ4rykRISDQniGW8JysnamxxoY"
genai.configure(api_key=API_KEY)

# Dùng model mới
model = genai.GenerativeModel("gemini-1.5-flash-latest")

response = model.generate_content("Tạo nội dung bài giảng về nguồn gốc Trái Đất, có yếu tố STEM")
print(response.text)
