# routes/document_routes.py
from flask import Blueprint, request, jsonify
from controllers.document_controller import (
    get_all_documents, get_document_by_id,
    create_document, update_document, delete_document
)

document_bp = Blueprint('document_bp', __name__)

@document_bp.route('/', methods=['GET'])
def get_documents():
    # Ở đây bạn sẽ cần xác thực người dùng (login_required)
    return get_all_documents()

@document_bp.route('/<int:doc_id>', methods=['GET'])
def get_single_document(doc_id):
    return get_document_by_id(doc_id)

@document_bp.route('/', methods=['POST'])
def create_doc():
    # Ở đây bạn sẽ cần xác thực người dùng
    return create_document()

@document_bp.route('/<int:doc_id>', methods=['PUT'])
def update_doc(doc_id):
    # Ở đây bạn sẽ cần xác thực người dùng và kiểm tra quyền sở hữu
    return update_document(doc_id)

@document_bp.route('/<int:doc_id>', methods=['DELETE'])
def delete_doc(doc_id):
    # Ở đây bạn sẽ cần xác thực người dùng và kiểm tra quyền sở hữu
    return delete_document(doc_id)