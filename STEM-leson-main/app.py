from flask import Flask
from models.user import db  # thêm dòng này
from routes.auth_routes import auth_bp
from routes.slide_routes import slide_bp
from routes.generate_routes import generate_bp
from config.config import Config
from flask import render_template 
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)      

# Config JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# 🔧 Cấu hình SQLite tạm (hoặc dùng database của bạn)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🔁 Khởi tạo db với app
db.init_app(app)

# Đăng ký các blueprint (route)
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(slide_bp, url_prefix='/api/slides')
app.register_blueprint(generate_bp, url_prefix='/api/generate')

# Route kiểm tra server
@app.route('/')
def index():
    return render_template('index.html')   # Gọi file trong folder template/


if __name__ == '__main__':
    app.run(debug=True)
