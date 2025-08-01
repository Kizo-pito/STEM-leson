import os

class Config:
    DEBUG = True
    SECRET_KEY = 'super-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API key Gemini (lấy từ biến môi trường hoặc để sẵn)
    GEMINI_API_KEY = os.getenv(
        'GEMINI_API_KEY',
        'AIzaSyA-EfORoQ5t5w7g2vOqebID7U14GeFmiqc'  # Dán API key Gemini của bạn vào đây
    )
