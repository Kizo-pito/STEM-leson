from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import google.generativeai as genai

generate_bp = Blueprint('generate', __name__)

# --- Model cấu hình ---
def get_model():
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY chưa được cấu hình")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-latest")

# --- API tạo dàn ý ---
@generate_bp.route('/outline', methods=['POST'])
def generate_outline():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Thiếu dữ liệu"}), 400
    try:
        model = get_model()
        response = model.generate_content(f"Hãy tạo dàn ý cho bài giảng: {text}")
        return jsonify({"input": text, "result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API tạo giáo án ---
@generate_bp.route('/lesson', methods=['POST'])
def generate_lesson():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Thiếu dữ liệu"}), 400
    try:
        model = get_model()
        response = model.generate_content(f"Hãy viết giáo án chi tiết cho: {text}")
        return jsonify({"input": text, "result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API tạo slide ---
@generate_bp.route('/slides', methods=['POST'])
def generate_slides():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Thiếu dữ liệu"}), 400
    try:
        model = get_model()
        response = model.generate_content(f"Hãy tạo slide trình bày cho bài giảng sau: {text}")
        return jsonify({"input": text, "result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API tóm tắt tài liệu ---
@generate_bp.route('/summarize', methods=['POST'])
def generate_summarize():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Thiếu dữ liệu"}), 400
    try:
        model = get_model()
        response = model.generate_content(f"Hãy tóm tắt nội dung sau: {text}")
        return jsonify({"input": text, "result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API chat từng câu (giống ChatGPT) ---
@generate_bp.route('/chat/message', methods=['POST'])
@jwt_required()
def chat_message():
    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Thiếu message"}), 400
    try:
        model = get_model()
        response = model.generate_content(message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API chat theo luồng: tạo giáo án từ hội thoại ---
@generate_bp.route('/chat/flow', methods=['POST'])
def chat_flow():
    data = request.json
    user_message = data.get("message", "")
    state = data.get("state", "ask_topic")

    try:
        model = get_model()

        if state == "ask_topic":
            reply = "Chào thầy/cô! Hôm nay bạn muốn dạy chủ đề gì?"
            next_state = "wait_topic"

        elif state == "wait_topic":
            response = model.generate_content(f"Hãy tạo dàn ý bài giảng cho chủ đề: {user_message}")
            outline = response.text
            reply = f"Đây là dàn ý gợi ý:\n{outline}\n\nBạn thấy ổn chưa? (Nhập 'Tiếp tục' để tạo giáo án hoặc chỉnh sửa nếu cần)"
            next_state = "confirm_outline"
            data_to_pass = {"outline": outline}

        elif state == "confirm_outline":
            if "tiếp tục" in user_message.lower():
                outline = data.get("outline", "")
                response = model.generate_content(f"Hãy viết giáo án chi tiết từ dàn ý sau:\n{outline}")
                lesson = response.text
                reply = f"Đây là giáo án chi tiết:\n{lesson}\n\nBạn muốn tạo slide không?"
                next_state = "confirm_lesson"
                data_to_pass = {"lesson": lesson}
            else:
                reply = "Bạn muốn chỉnh sửa dàn ý thế nào? Hãy nhập nội dung sửa."
                next_state = "edit_outline"

        elif state == "edit_outline":
            new_outline = user_message
            response = model.generate_content(f"Hãy viết giáo án chi tiết từ dàn ý sau:\n{new_outline}")
            lesson = response.text
            reply = f"Đây là giáo án mới dựa trên dàn ý đã sửa:\n{lesson}\n\nBạn muốn tạo slide không?"
            next_state = "confirm_lesson"
            data_to_pass = {"lesson": lesson}

        elif state == "confirm_lesson":
            if "có" in user_message.lower() or "vâng" in user_message.lower():
                lesson = data.get("lesson", "")
                response = model.generate_content(f"Hãy tạo slide trình bày cho bài giảng sau:\n{lesson}")
                slides = response.text
                reply = f"Dưới đây là slide trình bày:\n{slides}\n\nHoàn tất quá trình rồi nhé!"
                next_state = "done"
            else:
                reply = "Đã dừng tại bước giáo án. Bạn có thể yêu cầu tạo slide sau."
                next_state = "done"

        else:
            reply = "Kết thúc hội thoại. Nếu muốn bắt đầu lại, hãy nhập 'bắt đầu'."
            next_state = "ask_topic"

        return jsonify({
            "reply": reply,
            "next_state": next_state,
            **(data_to_pass if 'data_to_pass' in locals() else {})
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
