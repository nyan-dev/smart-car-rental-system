import os

class Config:
    """
    Application configuration class
    Database နဲ့ security settings တွေ ထားတဲ့ class
    """
    
    # Secret key for session management and CSRF protection
    # Session တွေကို encrypt လုပ်ဖို့ သုံးမယ့် secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # SQLite database file location
    # Database file ကို project folder အောက်က instance folder မှာ ထားမယ်
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///car_rental.db'
    
    # Disable modification tracking to save resources
    # SQLAlchemy ရဲ့ tracking feature ကို ပိတ်မယ် (လိုမှ မဟုတ်ဘူး)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder for car images (future use)
    # ကားပုံတွေ upload လုပ်မဲ့ folder
    UPLOAD_FOLDER = 'static/images'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
