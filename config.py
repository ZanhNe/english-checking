from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

# DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))
# DB_URL = f'{os.getenv('DB_DRIVER')}://{os.getenv('DB_USERNAME')}:{DB_PASSWORD}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4'


class Config:
    SECRET_KEY = 'sieu_bi_mat_ne'
    
    # SQLALCHEMY_DATABASE_URI = DB_URL
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECURITY_PASSWORD_SALT = "english_learning_system"
    # SECURITY_REGISTERABLE = True
    # SECURITY_PASSWORD_HASH = "bcrypt"   # Hashing password, Cần phải install thư viện bcrypt trước 
    # SECURITY_LOGIN_URL = "/dang-nhap"
    # SECURITY_LOGOUT_URL = "/dang-xuat"
    # SECURITY_REGISTER_URL = "/dang-ky"
    # SECURITY_POST_LOGIN_VIEW = "/trang-chu"
    # SECURITY_POST_LOGOUT_VIEW = "/trang-chu"
    # SECURITY_UNAUTHORIZED_VIEW = '/dang-nhap'

    # SECURITY_SEND_REGISTER_EMAIL = True

    # SECURITY_REGISTERABLE = True
    # SECURITY_CONFIRMABLE = True
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = ('EnglishSystem', os.getenv('MAIL_USERNAME'))
    # SECURITY_EMAIL_SENDER = os.getenv('MAIL_USERNAME')
    # MAIL_DEBUG = True
    # SECURITY_EMAIL_SUBJECT_CONFIRM = 'Yêu cầu xác nhận tài khoản'
