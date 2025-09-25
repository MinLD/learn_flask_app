# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Cấu hình cơ bản."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Cấu hình cho môi trường phát triển."""
    DEBUG = True

class ProductionConfig(Config):
    """Cấu hình cho môi trường sản phẩm."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URL', Config.SQLALCHEMY_DATABASE_URI)

# THÊM ĐOẠN NÀY VÀO CUỐI FILE
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}