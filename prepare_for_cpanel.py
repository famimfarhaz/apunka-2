#!/usr/bin/env python3
"""
cPanel Deployment Preparation Script
This script prepares the KPI GPT project for cPanel deployment
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_deployment_package():
    """Create a deployment-ready package for cPanel"""
    
    print("🚀 Preparing KPI GPT for cPanel deployment...")
    
    # Create deployment directory
    deploy_dir = Path("./deploy_package")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Files to include in deployment
    essential_files = [
        "app.py",
        "app.wsgi",
        "production_config.py",
        "requirements_cpanel.txt",
        ".htaccess",
        ".env.example",
        "kpi_gpt_rag.py",
        "groq_client.py",
        "vector_database.py",
        "semantic_retrieval.py",
        "ai_powered_kpi_gpt.py",
        "conversational_kpi_gpt.py",
        "conversation_context.py",
        "natural_language_processor.py",
        "ai_intent_recognizer.py",
        "data_preprocessor.py",
        "config.py",
        "kpi_data.txt",
        "README.md"
    ]
    
    # Directories to include
    essential_dirs = [
        "templates",
        "static"
    ]
    
    # Copy essential files
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            print(f"✅ Copied: {file}")
        else:
            print(f"⚠️  Warning: {file} not found")
    
    # Copy essential directories
    for dir_name in essential_dirs:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, deploy_dir / dir_name)
            print(f"✅ Copied directory: {dir_name}")
        else:
            print(f"⚠️  Warning: Directory {dir_name} not found")
    
    # Create deployment instructions
    instructions = """
# KPI GPT cPanel Deployment Instructions

## 📋 Pre-deployment Checklist:
1. ✅ Ensure your cPanel supports Python 3.8+
2. ✅ Have your Groq API key ready
3. ✅ Backup any existing website data

## 🚀 Deployment Steps:

### Step 1: Upload Files
1. Login to cPanel
2. Go to File Manager
3. Navigate to public_html (or your domain's root directory)
4. Upload all files from this package
5. Extract if uploaded as ZIP

### Step 2: Setup Python Application
1. In cPanel, go to "Python App" or "Setup Python App"
2. Click "Create Application"
3. Choose Python version (3.8+ recommended)
4. Set Application Root to your domain directory
5. Set Application URL to your domain
6. Set Application startup file to: app.wsgi
7. Set Application Entry Point to: application

### Step 3: Install Dependencies
1. In Python App settings, open "Virtual Environment"
2. Run: pip install -r requirements_cpanel.txt

### Step 4: Configure Environment Variables
1. In Python App, go to Environment Variables
2. Add: GROQ_API_KEY = your_groq_api_key_here
3. Add other variables from .env.example as needed

### Step 5: Test Application
1. Visit your domain
2. Check if the KPI GPT interface loads
3. Test a sample query

## 🔧 Troubleshooting:
- Check Error Logs in cPanel
- Ensure all dependencies are installed
- Verify Python version compatibility
- Check file permissions (644 for files, 755 for directories)

## 📞 Need Help?
Contact your hosting provider for Python/Flask support if issues persist.
"""
    
    # Write instructions
    with open(deploy_dir / "DEPLOYMENT_INSTRUCTIONS.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    # Create ZIP package
    zip_path = "KPI_GPT_cPanel_Deploy.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Deployment package created successfully!")
    print(f"📦 ZIP file: {zip_path}")
    print(f"📁 Deploy directory: {deploy_dir}")
    print("\n📋 Next steps:")
    print("1. Extract the ZIP file and review DEPLOYMENT_INSTRUCTIONS.txt")
    print("2. Upload files to your cPanel")
    print("3. Setup Python application in cPanel")
    print("4. Configure environment variables")
    print("5. Test your application")

if __name__ == "__main__":
    create_deployment_package()
