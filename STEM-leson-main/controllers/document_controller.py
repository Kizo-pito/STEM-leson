# controllers/document_controller.py
from flask import request, jsonify
from app import db
from models.document import Document
# from flask_jwt_extended import jwt_required, get_jwt_identity # Cần nếu dùng JWT

def get_all_documents():
    # current_user_id = get_jwt_identity() # Lấy ID người dùng từ JWT
    # documents = Document.query.filter_by(user_id=current_user_id).all()
    # Để test, lấy tất cả documents
    documents = Document.query.all()
    output = []
    for doc in documents:
        output.append({
            'id': doc.id,
            'title': doc.title,
            'content': doc.content,
            'user_id': doc.user_id,
            'created_at': doc.created_at.isoformat()
        })
    return jsonify(output), 200

def get_document_by_id(doc_id):
    document = Document.query.get(doc_id)
    if not document:
        return jsonify({'message': 'Document not found'}), 404
    # Kiểm tra quyền sở hữu nếu có xác thực
    return jsonify({
        'id': document.id,
        'title': document.title,
        'content': document.content,
        'user_id': document.user_id,
        'created_at': document.created_at.isoformat()
    }), 200

def create_document():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    # user_id = get_jwt_identity() # Lấy ID người dùng từ JWT

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    # Để test, dùng user_id tạm thời hoặc tạo user đầu tiên
    # Giả sử bạn có user_id = 1
    new_doc = Document(title=title, content=content, user_id=1) # Đặt user_id cứng để test
    db.session.add(new_doc)
    db.session.commit()
    return jsonify({'message': 'Document created', 'id': new_doc.id}), 201

def update_document(doc_id):
    document = Document.query.get(doc_id)
    if not document:
        return jsonify({'message': 'Document not found'}), 404

    # Kiểm tra quyền sở hữu (nếu user_id của doc != current_user_id, trả về 403 Forbidden)

    data = request.get_json()
    document.title = data.get('title', document.title)
    document.content = data.get('content', document.content)
    db.session.commit()
    return jsonify({'message': 'Document updated'}), 200

def delete_document(doc_id):
    document = Document.query.get(doc_id)
    if not document:
        return jsonify({'message': 'Document not found'}), 404

    # Kiểm tra quyền sở hữu

    db.session.delete(document)
    db.session.commit()
    return jsonify({'message': 'Document deleted'}), 200