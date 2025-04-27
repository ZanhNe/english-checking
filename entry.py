from app import create_app 
from flask import render_template


flask_app = create_app() 


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__': #Để khởi tạo chạy ứng dụng
    flask_app.run(port=5000) 

    




