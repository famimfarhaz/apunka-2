#!/usr/bin/env python3
"""
KPI GPT Web UI Launcher
Created by: Famim Farhaz

Easy launcher script for the KPI GPT web interface
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import sentence_transformers
        import chromadb
        import groq
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing web UI dependencies...")
    
    requirements_file = Path(__file__).parent / "requirements_web.txt"
    
    if requirements_file.exists():
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ])
            print("✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    else:
        print("❌ requirements_web.txt not found")
        return False

def check_data_file():
    """Check if KPI data file exists"""
    data_file = Path(__file__).parent / "kpi_data.txt"
    if not data_file.exists():
        print("⚠️  Warning: kpi_data.txt not found!")
        print("   Make sure your KPI data file is in the same directory as this script.")
        print("   The system will try to continue, but you may need to add your data.")
        return False
    return True

def check_env_file():
    """Check if .env file exists and create a basic one if not"""
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("📝 Creating basic .env file...")
        env_content = """# KPI GPT Configuration
# Add your Groq API key here
GROQ_API_KEY=your_groq_api_key_here

# Optional: Customize these settings
DATA_FILE=kpi_data.txt
VECTOR_DB_PATH=./vector_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
GROQ_MODEL=llama3-8b-8192
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_RETRIEVAL_RESULTS=5
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env file")
        print("📝 Please edit .env file and add your Groq API key!")
        return False
    return True

def main():
    """Main launcher function"""
    print("🚀 KPI GPT Web UI Launcher")
    print("=" * 50)
    print("Created by: Famim Farhaz")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        print("📦 Some dependencies are missing. Installing...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements_web.txt")
            return False
    else:
        print("✅ All dependencies are installed!")
    
    # Check data file
    print("\n📁 Checking data files...")
    check_data_file()
    
    # Check environment file
    print("\n⚙️  Checking configuration...")
    env_exists = check_env_file()
    
    if not env_exists:
        print("\n⚠️  Please configure your .env file first!")
        print("   1. Open the .env file in a text editor")
        print("   2. Add your Groq API key")
        print("   3. Run this script again")
        
        # Ask if user wants to continue anyway
        try:
            choice = input("\n🤔 Do you want to continue anyway? (y/n): ").strip().lower()
            if choice not in ['y', 'yes']:
                print("👋 Setup stopped. Configure your .env file and try again!")
                return False
        except KeyboardInterrupt:
            print("\n👋 Setup cancelled!")
            return False
    
    # Launch the web interface
    print("\n🌐 Starting KPI GPT Web Interface...")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app, startup
        
        print("📚 Initializing RAG system...")
        if startup():
            print("✅ System initialized successfully!")
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(2)
                webbrowser.open('http://localhost:5000')
            
            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            print("\n🎉 KPI GPT Web Interface is starting...")
            print("📱 Opening browser at: http://localhost:5000")
            print("⚡ Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Run Flask app
            app.run(
                host='0.0.0.0',
                port=5000,
                debug=False,
                threaded=True
            )
        else:
            print("❌ Failed to initialize RAG system")
            print("   Check your configuration and data files")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import required modules: {e}")
        print("   Make sure all files are in the correct location")
        return False
    except KeyboardInterrupt:
        print("\n\n👋 KPI GPT Web Interface stopped!")
        print("Thanks for using KPI GPT! 🎓")
        return True
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        print("   Please check the error message above and try again")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPress Enter to exit...")
        sys.exit(1)
