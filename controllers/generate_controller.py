# controllers/generate_controller.py
from flask import request, jsonify
from services.gemini_service import generate_outline, generate_slide_content, generate_lesson_from_gemini, summarize_with_ai
from flask_jwt_extended import get_jwt_identity
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

def generate_specific_slide_content():
    data = request.get_json()
    outline_point = data.get('outline_point')
    context = data.get('context', '') # Thêm context để AI hiểu rõ hơn
    if not outline_point:
        return jsonify({'message': 'Missing outline_point'}), 400
    try:
        content = generate_slide_content(outline_point, context)
        return jsonify({'content': content}), 200
    except Exception as e:
        return jsonify({'message': f'Error generating slide content: {str(e)}'}), 500
def generate_lesson_content():
    current_user_id = get_jwt_identity() # Lấy ID người dùng hiện tại (nếu bạn muốn lưu bài giảng vào database sau này)
    data = request.get_json()

    # Lấy các thông tin cần thiết từ request JSON
    grade = data.get('grade')
    subject = data.get('subject')
    topic = data.get('topic')
    specific_requests = data.get('requests') # Yêu cầu bổ sung từ người dùng (tùy chọn)

    # Kiểm tra dữ liệu đầu vào
    if not grade or not subject or not topic:
        return jsonify({'message': 'Missing grade, subject, or topic in request'}), 400

    # Xây dựng prompt cho AI
    prompt = f"Tạo một bài giảng chi tiết cho học sinh lớp {grade}, môn {subject} về chủ đề '{topic}'. "
    if specific_requests:
        prompt += f"Yêu cầu cụ thể: {specific_requests}. "
    prompt += "Bài giảng cần được trình bày một cách rõ ràng, dễ hiểu, và phù hợp với trình độ học sinh lớp đó. Trả lời trực tiếp nội dung bài giảng, không bao gồm lời chào hay kết thúc."

def summarize_document():
    data = request.get_json()
    text = data.get("text", "")
    content = summarize_with_ai(text)
    return jsonify({"summary": content})
    try:
        # Gọi service để tương tác với Gemini API
        lesson_text = generate_lesson_from_gemini(prompt)

        # Trả về kết quả cho client
        return jsonify({'lesson_text': lesson_text, 'topic': topic, 'grade': grade, 'subject': subject}), 200
    except Exception as e:
        # Xử lý lỗi nếu có vấn đề với Gemini API hoặc logic
        print(f"Error in generate_lesson_content: {e}") # In lỗi ra console để debug
        return jsonify({'message': f'Error generating lesson: {str(e)}'}), 500    
