import os

class Config:
    DEBUG = True              # Bật/tắt chế độ debug
    SECRET_KEY = 'bacc1b5c901001395109954485919965504f87591da55ca9fd7de0bfaef2bf3f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'   # Kết nối SQLite
# hoặc MySQL / PostgreSQL
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/dbname'

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Tắt cảnh báo theo dõi thay đổi
    SESSION_COOKIE_SECURE = True        # Cookie chỉ truyền qua HTTPS
    PERMANENT_SESSION_LIFETIME = 3600   # Thời gian tồn tại của session (giây)
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # Giới hạn 16MB

    API_KEY = 'your_api_key'
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBld67u3T-_DKfoyLh3WYrr4N2YRGpGYCo')  # Lấy từ biến môi trường
    CORS_HEADERS = 'Content-Type'  # Cấu hình CORS nếu cần thiết
