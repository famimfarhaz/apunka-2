#!/usr/bin/python3.10

"""
WSGI Configuration for KPI GPT RAG System on PythonAnywhere
This file serves as the main entry point for PythonAnywhere hosting.

IMPORTANT: 
- This file should be renamed to match your PythonAnywhere username
- For example: if your username is 'yourusername', name this file 'yourusername_flask_app.py'
- Then in the PythonAnywhere web tab, set the source code to '/home/yourusername/mysite/yourusername_flask_app.py'
"""

import sys
import os

# Add your project directory to the Python path
# Replace 'yourusername' with your actual PythonAnywhere username
project_home = '/home/yourusername/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'
os.environ['PYTHONPATH'] = project_home

# Import your Flask application
# This imports from app.py in your project directory
try:
    from app import app as application
    
    # Additional configuration for PythonAnywhere
    application.config['DEBUG'] = False
    application.config['TESTING'] = False
    
    # Ensure the app can find its data files
    if hasattr(application, 'config'):
        application.config['PROJECT_ROOT'] = project_home
        
except ImportError as e:
    # If import fails, create a simple error application
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def import_error():
        return f"""
        <h1>Import Error</h1>
        <p>Failed to import the KPI GPT application: {str(e)}</p>
        <p>Please check that all files are uploaded and the Python path is correct.</p>
        <p>Project path: {project_home}</p>
        <p>Python path: {sys.path}</p>
        """

# This is required for PythonAnywhere
if __name__ == "__main__":
    application.run(debug=False)
