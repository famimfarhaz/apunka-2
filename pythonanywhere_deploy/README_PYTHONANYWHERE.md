# KPI GPT - PythonAnywhere Deployment Package

## 📦 What's Included

This deployment package contains everything you need to host your KPI GPT application on PythonAnywhere:

### Core Application Files
- `app.py` - Main Flask application
- `kpi_gpt_rag.py` - RAG system core
- `kpi_data.txt` - KPI knowledge base
- All supporting Python modules

### PythonAnywhere-Specific Files
- `flask_app.py` - PythonAnywhere WSGI entry point (rename to match your username)
- `requirements.txt` - Python dependencies optimized for PythonAnywhere
- `.env.template` - Environment variables template
- `PYTHONANYWHERE_DEPLOYMENT_GUIDE.md` - **READ THIS FIRST!**

### Web Interface
- `templates/index.html` - Web UI template
- `static/` - CSS and JavaScript files

## 🚀 Quick Start

### **IMPORTANT: Read the Complete Guide First**
👉 **Open `PYTHONANYWHERE_DEPLOYMENT_GUIDE.md`** for detailed step-by-step instructions!

### Summary:
1. **Get Groq API key**: Sign up at console.groq.com
2. **Upload files** to PythonAnywhere `/home/yourusername/mysite/`
3. **Rename** `flask_app.py` to `yourusername_flask_app.py`
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Configure environment**: Copy `.env.template` to `.env` and add your API key
6. **Set up web app** in PythonAnywhere's Web tab
7. **Test** your application

## 📋 Requirements

- PythonAnywhere account (free or paid)
- Groq API key for AI processing  
- Python 3.8+ (3.10 recommended)

## 💡 Key Features

Your deployed KPI GPT will include:
- ✨ Interactive web chat interface
- 🤖 AI-powered answers about KPI
- 💬 Real-time streaming responses
- 📱 Modern, responsive design
- 🚀 Automatic system initialization

## 📞 Need Help?

1. **Start Here**: Read `PYTHONANYWHERE_DEPLOYMENT_GUIDE.md`
2. **PythonAnywhere Docs**: Check their Flask deployment guides
3. **Error Logs**: Use PythonAnywhere's Web tab to check logs

## ⚠️ Important Notes

- **Free Account**: Limited CPU time, perfect for testing
- **Paid Account**: Better performance, recommended for production
- **First Load**: System takes time to initialize AI components
- **API Key Required**: Application won't work without Groq API key

---

**Created by:** Famim Farhaz  
**Project:** KPI GPT RAG System  
**Platform:** PythonAnywhere Deployment

🎯 **Goal**: Get your KPI GPT live on the web!
