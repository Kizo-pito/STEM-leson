# config/gemini.py
import google.generativeai as genai

# ⚠️ Đổi khóa này thành API key của bạn
API_KEY = "AIzaSyA-EfORoQ5t5w7g2vOqebID7U14GeFmiqc"

def get_gemini_model():
    genai.configure(api_key=API_KEY)
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
    )
    return model
