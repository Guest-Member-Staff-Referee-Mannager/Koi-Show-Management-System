from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import random
import string
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thay đổi secret key cho bảo mật

# Cấu hình kết nối MySQL
db_config = {
    'user': 'root',
    'password': 'quoctri1014',  # Thay bằng mật khẩu MySQL của bạn
    'host': '127.0.0.1',
    'database': 'koi_exhibition'
}

# Hàm kết nối tới cơ sở dữ liệu MySQL
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Hàm tạo mã CAPTCHA
def generate_captcha(length=6):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Hàm kiểm tra tên
def validate_name(name):
    return name.istitle()  # Kiểm tra xem tên có viết hoa chữ cái đầu không

# Hàm kiểm tra email
def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email) is not None

# Hàm kiểm tra mật khẩu
def validate_password(password):
    return (len(password) >= 8 and 
            any(char.isdigit() for char in password) and 
            password[0].isupper())

# Hàm kiểm tra số điện thoại
def validate_phone(phone):
    return re.match(r'^0\d{9}$', phone) is not None

# Route Trang chủ
@app.route('/')
def home():
    return render_template('index.html')  # Thay đổi thành template của bạn
@app.route('/add-koi', methods=['GET', 'POST'])
def add_koi():
    if 'user_id' not in session:  # Kiểm tra xem người dùng đã đăng nhập chưa
        flash("Bạn cần đăng nhập để thêm cá Koi.", "danger")
        return redirect(url_for('login'))

    errors = {}
    koi_name = ""
    koi_type = ""
    koi_age = ""
    koi_description = ""

    if request.method == 'POST':
        koi_name = request.form.get('koi_name', '').strip()
        koi_type = request.form.get('koi_type', '').strip()
        koi_age = request.form.get('koi_age', '').strip()
        koi_description = request.form.get('koi_description', '').strip()

        # Kiểm tra dữ liệu cá Koi
        if not koi_name:
            errors['koi_name'] = "Tên cá Koi không được để trống."
        if not koi_type:
            errors['koi_type'] = "Giống cá Koi không được để trống."
        if not koi_age.isdigit():
            errors['koi_age'] = "Tuổi cá Koi phải là một số."

        # Nếu có lỗi, trả về trang thêm cá Koi với thông báo lỗi
        if errors:
            return render_template('add-koi.html', errors=errors, koi_name=koi_name, koi_type=koi_type, koi_age=koi_age, koi_description=koi_description)

        # Lưu thông tin cá Koi vào cơ sở dữ liệu
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO koi (name, type, age, description) VALUES (%s, %s, %s, %s)',
                (koi_name, koi_type, koi_age, koi_description)
            )
            conn.commit()
            flash("Thêm cá Koi thành công!", "success")
            return redirect(url_for('add_koi'))  # Redirect về trang thêm cá Koi
        except Exception as e:
            conn.rollback()
            errors['database'] = "Lỗi trong quá trình lưu dữ liệu. Vui lòng thử lại."
        finally:
            conn.close()

    return render_template('add-koi.html', errors=errors, koi_name=koi_name, koi_type=koi_type, koi_age=koi_age, koi_description=koi_description)
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/exhibition')
def exhibition():  # Đổi tên hàm thành 'exhibition'
    return render_template('exhibition.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    name = ""
    phone = ""
    email = ""
    password = ""
    captcha = ""

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        captcha = request.form.get('captcha', '').strip()

        # Kiểm tra CAPTCHA
        if captcha != session.get('captcha'):
            errors['captcha'] = "Mã xác thực không đúng."

        # Kiểm tra tên
        if not name.istitle():
            errors['name'] = "Tên phải viết hoa chữ cái đầu."

        # Kiểm tra số điện thoại
        if not (phone.isdigit() and phone.startswith('0') and len(phone) == 10):
            errors['phone'] = "Số điện thoại không hợp lệ."

        # Kiểm tra email
        if not email.endswith("@gmail.com"):
            errors['email'] = "Email phải có định dạng @gmail.com."

        # Kiểm tra mật khẩu
        if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            errors['password'] = "Mật khẩu phải có ít nhất 8 ký tự, một chữ cái đầu viết hoa và một số."

        # Nếu có lỗi, trả về trang đăng ký với thông báo lỗi
        if errors:
            session['captcha'] = generate_captcha()  # Tạo CAPTCHA mới
            return render_template('register.html', errors=errors, name=name, phone=phone, email=email, captcha=session['captcha'])

        # Lưu thông tin vào cơ sở dữ liệu
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (name, phone, email, password) VALUES (%s, %s, %s, %s)',
                (name, phone, email, generate_password_hash(password))
            )
            conn.commit()
            flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            errors['database'] = "Lỗi trong quá trình lưu dữ liệu. Vui lòng thử lại."
        finally:
            conn.close()

    # GET: Hiển thị trang đăng ký và tạo CAPTCHA mới
    session['captcha'] = generate_captcha()
    return render_template('register.html', errors=errors, name=name, phone=phone, email=email, captcha=session['captcha'])
# Route Đăng Nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name', '')  # Sử dụng name làm tên đăng nhập
        password = request.form.get('password', '')
        captcha = request.form.get('captcha', '')

        # Kiểm tra CAPTCHA
        if captcha != session.get('captcha'):
            return "Mã xác thực không đúng"

        # Xử lý đăng nhập (kiểm tra name và password trong cơ sở dữ liệu)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[4], password):  # So sánh mật khẩu đã mã hóa
            session['user_id'] = user[0]  # Lưu ID người dùng vào session
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('add_koi'))  # Redirect đến trang thêm cá Koi
        else:
            return "Đăng nhập không thành công"

    # Tạo mã CAPTCHA mới
    session['captcha'] = generate_captcha()
    return render_template('login.html', captcha=session['captcha'])  # Trả về trang login.html
# Route Quên Mật Khẩu
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    errors = {}
    name = ""
    email = ""
    phone = ""

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        captcha = request.form.get('captcha', '').strip()

        # Kiểm tra CAPTCHA
        if captcha != session.get('captcha'):
            errors['captcha'] = "Mã xác thực không đúng"

        # Kiểm tra thông tin người dùng
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            errors['name'] = "Tên người dùng không tồn tại."
        else:
            # Kiểm tra email
            if user[3].strip() != email:  # user[3] là cột email
                errors['email'] = "Email không khớp với tên người dùng."
            # Kiểm tra số điện thoại
            if user[2].strip() != phone:  # user[2] là cột phone
                errors['phone'] = "Số điện thoại không khớp với tên người dùng."

        # Nếu có lỗi, trả về trang quên mật khẩu với thông báo lỗi
        if errors:
            return render_template('forgot_password.html', captcha=session['captcha'], errors=errors, name=name, email=email, phone=phone)

        # Nếu không có lỗi, chuyển hướng đến trang thay đổi mật khẩu
        flash("Thông tin chính xác. Vui lòng đặt lại mật khẩu.", "success")
        return redirect(url_for('change_password', username=name))

    # Tạo mã CAPTCHA mới mỗi khi truy cập trang
    session['captcha'] = generate_captcha()
    return render_template('forgot_password.html', captcha=session['captcha'], errors=errors, name=name, email=email, phone=phone)

# Route Thay Đổi Mật Khẩu
@app.route('/change_password/<username>', methods=['GET', 'POST'])
def change_password(username):
    if request.method == 'POST':
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Kiểm tra mật khẩu mới
        if new_password != confirm_password:
            flash("Mật khẩu không khớp", "danger")
        elif not validate_password(new_password):
            flash("Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa và số", "danger")
        else:
            # Cập nhật mật khẩu trong cơ sở dữ liệu
            hashed_password = generate_password_hash(new_password)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = %s WHERE name = %s', (hashed_password, username))
            conn.commit()
            conn.close()
            flash("Mật khẩu đã được thay đổi thành công", "success")
            return redirect(url_for('login'))

    return render_template('change_password.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)  # Chạy ứng dụng Flask trong chế độ gỡ lỗi