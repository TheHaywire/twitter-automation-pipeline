import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    X_CLIENT_ID = os.getenv('X_CLIENT_ID')
    X_CLIENT_SECRET = os.getenv('X_CLIENT_SECRET')
    X_REDIRECT_URI = os.getenv('X_REDIRECT_URI')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    LOG_DB_PATH = os.getenv('LOG_DB_PATH', 'logs/agentic_research.db')
    SCHEDULE_TIMES = os.getenv('SCHEDULE_TIMES', '09:00,15:00,21:00').split(',')
    DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'
    STRICTNESS = os.getenv('STRICTNESS', 'strict').lower()  # 'strict', 'medium', 'lenient'
