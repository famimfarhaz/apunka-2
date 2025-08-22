"""
Production Configuration for KPI GPT RAG System
Optimized for cPanel hosting environment
"""
import os

class ProductionConfig:
    """Production configuration with optimized settings for cPanel"""
    
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-production-secret-key-here'
    DEBUG = False
    TESTING = False
    
    # Application Settings
    TEMPLATES_AUTO_RELOAD = False
    
    # Database Settings (if using database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    # KPI GPT Specific Settings
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    DATA_FILE = os.environ.get('DATA_FILE', 'kpi_data.txt')
    VECTOR_DB_PATH = os.environ.get('VECTOR_DB_PATH', './vector_db')
    EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama3-8b-8192')
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', '200'))
    MAX_RETRIEVAL_RESULTS = int(os.environ.get('MAX_RETRIEVAL_RESULTS', '5'))
    TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.7'))

# Configuration dictionary
config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}
