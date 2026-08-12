import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-grocery-key-12345'
    
    # --- NEON LIVE CLOUD DATABASE ---
    # Replace the string below with the exact URL you just copied from your Neon dashboard
    NEON_URL = 'postgresql://neondb_owner:npg_9VfwTxgYUe0h@ep-snowy-boat-aoxrg945.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or NEON_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    
    @staticmethod
    def init_app(app):
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)