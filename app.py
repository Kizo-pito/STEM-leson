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
    return render_template('test.html')   # Gọi file trong folder template/


@app.route('/dang-ky')
def dang_ky():
    return render_template('dang-ky.html')

@app.route('/goi-y')
def goi_y():
    return render_template('goi-y.html')

@app.route('/ho-so')
def ho_so():
    return render_template('ho-so.html')

@app.route('/lua-chon')
def lua_chon():
    return render_template('lua-chon.html')

@app.route('/cong-dong')
def cong_dong():
    return render_template('cong-dong.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/man-hinh-chinh')
def man_hinh_chinh():
    return render_template('màn hình chính.html')  # tên này có dấu cách -> nên sửa!


if __name__ == '__main__':
    app.run(debug=True)
