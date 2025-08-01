import google.generativeai as genai
from flask import Blueprint, request, jsonify, current_app

generate_bp = Blueprint('generate', __name__)

def get_model():
    api_key = current_app.config['GEMINI_API_KEY']
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-latest")

# Tạo dàn ý
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

# Tạo bài giảng
@generate_bp.route('/lesson', methods=['POST'])
def generate_lesson():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Thiếu dữ liệu"}), 400

    try:
        model = get_model()
        response = model.generate_content(f"Hãy viết nội dung bài giảng chi tiết cho: {text}")
        return jsonify({"input": text, "result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tạo slide
@generate_bp.route('/slides', methods=['POST'])
def generate_slides():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Thiếu dữ liệu"}), 400

    try:
        model = get_model()
        response = model.generate_content(f"Hãy tạo các slide cho bài giảng: {text}")
        return jsonify({"input": text, "result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tóm tắt tài liệu
@generate_bp.route('/summarize', methods=['POST'])
def generate_summarize():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Thiếu dữ liệu"}), 400

    try:
        model = get_model()
        response = model.generate_content(f"Hãy tóm tắt ngắn gọn: {text}")
        return jsonify({"input": text, "result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
