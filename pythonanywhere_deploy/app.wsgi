#!/usr/bin/python3
"""
WSGI Configuration for KPI GPT RAG System
This file is the entry point for cPanel hosting
"""
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask application
from app import app

# This is what cPanel will use as the WSGI application
application = app

if __name__ == "__main__":
    application.run()
