from flask import Blueprint, request, jsonify
from controllers.slide_controller import generate_slide_from_prompt

slide_bp = Blueprint('slide_bp', __name__)

@slide_bp.route('/generate', methods=['POST'])
def generate_slide():
    data = request.get_json()
    prompt = data.get('prompt')
    content = generate_slide_from_prompt(prompt)
    return jsonify({'content': content})