from flask import request, jsonify
from services.gemini_service import (
    generate_outline,
    generate_slide_content,
    generate_lesson_from_gemini,
    summarize_with_ai,
    get_gemini_model  # 👈 cần thêm nếu chưa có
)
from flask_jwt_extended import get_jwt_identity

# ---------- 1. Dàn ý bài giảng ----------
def generate_document_outline():
    data = request.get_json()
    topic = data.get('topic')
    if not topic:
        return jsonify({'message': 'Missing topic'}), 400
    try:
        outline = generate_outline(topic)
        return jsonify({'outline': outline}), 200
    except Exception as e:
        return jsonify({'message': f'Error generating outline: {str(e)}'}), 500

# ---------- 2. Slide chi tiết cho từng mục ----------
def generate_specific_slide_content():
    data = request.get_json()
    outline_point = data.get('outline_point')
    context = data.get('context', '')  # Optional
    if not outline_point:
        return jsonify({'message': 'Missing outline_point'}), 400
    try:
        content = generate_slide_content(outline_point, context)
        return jsonify({'content': content}), 200
    except Exception as e:
        return jsonify({'message': f'Error generating slide content: {str(e)}'}), 500

# ---------- 3. Sinh giáo án ----------
def generate_lesson_content():
    current_user_id = get_jwt_identity()  # Nếu cần gắn với user
    data = request.get_json()

    grade = data.get('grade')
    subject = data.get('subject')
    topic = data.get('topic')
    specific_requests = data.get('requests')

    if not grade or not subject or not topic:
        return jsonify({'message': 'Missing grade, subject, or topic'}), 400

    prompt = f"Tạo một giáo án chi tiết cho học sinh lớp {grade}, môn {subject} về chủ đề '{topic}'. "
    if specific_requests:
        prompt += f"Yêu cầu cụ thể: {specific_requests}. "
    prompt += "Giáo án cần có: mục tiêu, chuẩn bị, tiến trình dạy học, hoạt động GV & HS, thời lượng. Trình bày rõ ràng, dễ hiểu."

    try:
        lesson_text = generate_lesson_from_gemini(prompt)
        return jsonify({
            'lesson_text': lesson_text,
            'topic': topic,
            'grade': grade,
            'subject': subject
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error generating lesson: {str(e)}'}), 500

# ---------- 4. Tóm tắt tài liệu ----------
def summarize_document():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({'message': 'Missing text'}), 400
    try:
        content = summarize_with_ai(text)
        return jsonify({"summary": content}), 200
    except Exception as e:
        return jsonify({'message': f'Error summarizing document: {str(e)}'}), 500

# ---------- 5. Chat tương tác AI ----------
def interactive_ai_chat():
    data = request.get_json()
    message = data.get('message')
    if not message:
        return jsonify({'message': 'Missing message'}), 400

    try:
        model = get_gemini_model()
        response = model.generate_content(message)
        return jsonify({'reply': response.text.strip()}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
