import google.generativeai as genai
from flask import current_app

def configure_gemini():
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not configured in app.config")
    genai.configure(api_key=api_key)

def generate_outline(topic):
    configure_gemini()
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Tạo một dàn ý chi tiết cho bài thuyết trình/tài liệu về chủ đề: {topic}"
    response = model.generate_content(prompt)
    return response.text

def generate_slide_content(outline_point, context=""):
    configure_gemini()
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Viết nội dung chi tiết cho một slide/phần dựa trên dàn ý: '{outline_point}'. Context: {context}"
    response = model.generate_content(prompt)
    return response.text

def generate_lesson_from_gemini(prompt: str) -> str:
    configure_gemini()
    model = genai.GenerativeModel('gemini-pro')
    print("📡 Gửi prompt tới Gemini:", prompt)
    response = model.generate_content(prompt)
    print("📥 Kết quả từ Gemini:", response.text)
    return response.text

def summarize_with_ai(text):
    configure_gemini()
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Tóm tắt nội dung sau: {text}"
    response = model.generate_content(prompt)
    return response.text
import re

def parse_markdown_to_json(markdown_text: str):
    slides = []
    current_slide = None

    lines = markdown_text.splitlines()
    for line in lines:
        if re.match(r"\*\*Slide \d+:.*\*\*", line):
            if current_slide:
                slides.append(current_slide)
            current_slide = {
                "title": re.sub(r"^\*\*|\*\*$", "", line).strip(),
                "content": ""
            }
        elif current_slide:
            current_slide["content"] += line + "\n"

    if current_slide:
        slides.append(current_slide)
    return {"slides": slides}
