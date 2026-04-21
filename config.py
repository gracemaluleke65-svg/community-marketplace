import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security - CRITICAL for production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required for production!")
    
    # Database - PostgreSQL on Render
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        # Fallback to SQLite for local development only
        if os.environ.get('FLASK_ENV') == 'development':
            DATABASE_URL = 'sqlite:///community_marketplace.db'
            print("WARNING: Using SQLite. Set DATABASE_URL for production!")
        else:
            raise ValueError("DATABASE_URL environment variable is required!")
    
    # Fix for Render's PostgreSQL URLs (postgres:// vs postgresql://)
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Production database pool settings for PostgreSQL
    if 'postgresql' in DATABASE_URL:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'pool_timeout': 30,
            'max_overflow': 20,
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
        }
    
    # Table prefix (optional, kept for compatibility)
    TABLE_PREFIX = 'CMP_'
    
    # Cloudinary - optional but recommended
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    
    # Stripe - required for payments
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
    
    # Session security (will be overridden for production in app.py)
    SESSION_COOKIE_SECURE = False  # Set True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File upload limits
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    
    # Flask environment
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
    
    @classmethod
    def validate(cls):
        """Validate critical configuration for production"""
        if cls.FLASK_ENV == 'production':
            required = ['SECRET_KEY', 'DATABASE_URL', 'STRIPE_PUBLISHABLE_KEY', 'STRIPE_SECRET_KEY']
            missing = [key for key in required if not getattr(cls, key)]
            if missing:
                raise ValueError(f"Missing required config: {', '.join(missing)}")
            print("Configuration validated successfully!")