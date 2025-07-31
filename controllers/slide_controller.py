# controllers\slide_controller.py
from services.gemini_service import generate_slide_content # Sửa lại tên service và tên hàm

def generate_slide_from_prompt(prompt: str):
    if not prompt:
        return "Không có prompt được gửi."
    return generate_slide_content(prompt)
