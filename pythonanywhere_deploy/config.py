"""
Configuration Module for KPI GPT RAG System
Created by: Famim Farhaz

This module contains configuration settings and utilities
for the KPI GPT RAG system.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for KPI GPT RAG system"""
    
    # Groq API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Vector Database Configuration
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "kpi_documents")
    
    # Data Processing Configuration
    DATA_FILE = os.getenv("DATA_FILE", "kpi_data.txt")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Retrieval Configuration
    MAX_RETRIEVAL_RESULTS = int(os.getenv("MAX_RETRIEVAL_RESULTS", "5"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.1"))
    
    # Application Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "kpi_gpt_rag.log")
    
    # System Information
    SYSTEM_NAME = "KPI GPT RAG System"
    VERSION = "1.0.0"
    CREATOR = "Famim Farhaz"
    INSTITUTE = "Khulna Polytechnic Institute"
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return {
            'groq': {
                'api_key': cls.GROQ_API_KEY,
                'model': cls.GROQ_MODEL,
                'temperature': cls.TEMPERATURE,
                'max_tokens': cls.MAX_TOKENS
            },
            'embedding': {
                'model': cls.EMBEDDING_MODEL
            },
            'database': {
                'path': cls.VECTOR_DB_PATH,
                'collection_name': cls.COLLECTION_NAME
            },
            'data_processing': {
                'data_file': cls.DATA_FILE,
                'chunk_size': cls.CHUNK_SIZE,
                'chunk_overlap': cls.CHUNK_OVERLAP
            },
            'retrieval': {
                'max_results': cls.MAX_RETRIEVAL_RESULTS,
                'similarity_threshold': cls.SIMILARITY_THRESHOLD
            },
            'system': {
                'name': cls.SYSTEM_NAME,
                'version': cls.VERSION,
                'creator': cls.CREATOR,
                'institute': cls.INSTITUTE
            }
        }
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate configuration settings"""
        validation = {}
        
        # Check Groq API key
        validation['groq_api_key'] = bool(cls.GROQ_API_KEY)
        
        # Check data file exists
        validation['data_file_exists'] = os.path.exists(cls.DATA_FILE)
        
        # Check chunk configuration
        validation['chunk_config'] = (cls.CHUNK_SIZE > 0 and 
                                     cls.CHUNK_OVERLAP >= 0 and 
                                     cls.CHUNK_OVERLAP < cls.CHUNK_SIZE)
        
        # Check retrieval configuration
        validation['retrieval_config'] = (cls.MAX_RETRIEVAL_RESULTS > 0 and 
                                         0 <= cls.SIMILARITY_THRESHOLD <= 1)
        
        return validation
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        config = cls.get_config_dict()
        
        print("🔧 KPI GPT RAG System Configuration")
        print("=" * 40)
        
        for section, settings in config.items():
            print(f"\n📋 {section.upper()}")
            for key, value in settings.items():
                if 'api_key' in key.lower():
                    display_value = f"{'*' * 10}...{value[-4:]}" if value else "Not set"
                else:
                    display_value = value
                print(f"   {key}: {display_value}")
        
        print("\n" + "=" * 40)
        
        # Show validation
        validation = cls.validate_config()
        print("\n✅ Configuration Validation:")
        for check, status in validation.items():
            status_emoji = "✅" if status else "❌"
            print(f"   {status_emoji} {check}: {status}")

# System prompts and templates
SYSTEM_PROMPTS = {
    'kpi_assistant': """You are KPI GPT, an AI assistant specifically designed for Khulna Polytechnic Institute (KPI). 
    You have comprehensive knowledge about the institute including:
    - Departments and their heads
    - Teaching staff and their contact information
    - Student information and class captains
    - Institute facilities and policies
    - College clubs and activities
    - Academic programs and curriculum
    
    Your role is to:
    1. Provide accurate information about KPI
    2. Help users find contact details and departmental information
    3. Answer queries about academic programs and facilities
    4. Be friendly, professional, and helpful
    
    Always base your responses on the provided context and indicate if information is not available.""",
    
    'search_enhancement': """Based on the user's query, identify the most relevant information from the context provided. 
    Focus on specific details like names, contact information, departments, and factual data about KPI."""
}

# Query templates
QUERY_TEMPLATES = {
    'contact_info': "Find contact information for {entity} at Khulna Polytechnic Institute",
    'department_info': "Provide information about the {department} department at KPI",
    'teacher_info': "Give details about teachers in {department} department",
    'general_info': "Tell me about {topic} at Khulna Polytechnic Institute"
}

if __name__ == "__main__":
    # Test configuration
    Config.print_config()
    
    # Test validation
    validation = Config.validate_config()
    print(f"\nConfiguration valid: {all(validation.values())}")
    
    if not all(validation.values()):
        print("⚠️  Please check the failed validation items above.")
