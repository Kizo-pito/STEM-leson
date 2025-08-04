from flask import request, jsonify
from services.gemini_service import (
    generate_outline,
    generate_slide_content,
    generate_lesson_from_gemini,
    summarize_with_ai,
)
from flask_jwt_extended import get_jwt_identity
from ultis.pdf_ultis import read_pdf_text


def generate_lesson_content():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    grade = data.get('grade')
    subject = data.get('subject')
    topic = data.get('topic')
    specific_requests = data.get('requests')

    if not grade or not subject or not topic:
        return jsonify({'message': 'Missing grade, subject, or topic'}), 400

    # ----- Đọc nội dung SGK liên quan -----
    # Tùy bạn map theo lớp/môn, ví dụ:
    pdf_path = "C:/Users/minhs/OneDrive/Videos/SGK KHTN 8 KNTT.pdf"
    try:
        book_content = read_pdf_text(pdf_path)
        book_excerpt = book_content[:5000]  # Cắt nếu quá dài (token limit)
    except Exception as e:
        return jsonify({'message': f'Error reading textbook: {str(e)}'}), 500

    # ----- Tạo prompt cho Gemini -----
    prompt = f"""
Nội dung sách giáo khoa lớp {grade}, môn {subject} như sau:
--- SGK ---
{book_excerpt}
--- Hết SGK ---

Dựa trên nội dung trên, hãy tạo một giáo án chi tiết cho học sinh lớp {8}, môn {subject}, chủ đề: '{topic}'.

Giáo án cần có:
- Tiêu đề các phần
- Mục tiêu
- Nội dung
- Ví dụ minh họa
- Hoạt động học sinh & giáo viên
- Gợi ý sử dụng hình ảnh/thí nghiệm (nếu có)
- Thời lượng mỗi phần
- Định dạng dưới dạng slide trình chiếu Markdown.

Yêu cầu thêm: {specific_requests or "Không có"}.
    """

    try:
        markdown_text = generate_lesson_from_gemini(prompt)
        slides_json = parse_markdown_to_json(markdown_text)

        return jsonify({
            'lesson': slides_json,
            'topic': topic,
            'grade': grade,
            'subject': subject
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error generating lesson: {str(e)}'}), 500



# ---------- Helper: Parse Markdown to JSON ----------
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
