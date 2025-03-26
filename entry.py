
from app import create_app #Dùng để import cái mình cần sử dụng trong hệ thống (nhưng với điều kiện nó phải được định nghĩa trước)
from app.extentions.extentions import user_datastore
from flask import render_template
from flask_security.signals import user_registered
#Ở đây là from app --> Tức là từ folder app (entry point) để trỏ tới trong folder app tìm hàm create_app()
from app.models.models import db


flask_app = create_app() #Lấy ra flask_app bởi hàm create_app() được định nghĩa trong ứng dụng

# ---- Gắn role sau khi đăng ký ----
@user_registered.connect_via(flask_app)
def assign_role(sender, user, **extra):
    role = user_datastore.find_role("USER")
    user_datastore.add_role_to_user(user, role)
    db.session.commit()


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__': #Để khởi tạo chạy ứng dụng
    flask_app.run(port=5000) 

    




