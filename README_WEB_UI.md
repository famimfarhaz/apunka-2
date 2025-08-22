# 🎓 KPI GPT - Modern Web Interface

A beautiful, modern black-themed web interface for the KPI GPT RAG system created by **Famim Farhaz**.

![KPI GPT Demo](https://img.shields.io/badge/Status-Ready-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0+-red)

## ✨ Features

- **🎨 Modern Black Theme**: Sleek, professional dark interface with gradients and animations
- **💬 Interactive Chat**: Real-time messaging with typing indicators and smooth animations
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **🔍 Smart Search**: Powered by your existing KPI GPT RAG system
- **📚 Source Citations**: Shows relevant sources for each AI response
- **⚙️ Settings Panel**: Customize your experience with dark mode, sound effects, and more
- **📊 System Status**: Real-time system monitoring and statistics
- **🚀 Easy Setup**: One-click launcher script for hassle-free deployment

## 🚀 Quick Start

### Option 1: Easy Launcher (Recommended)
```bash
python run_web_ui.py
```
The launcher will automatically:
- Check and install dependencies
- Verify your configuration
- Start the web server
- Open your browser to http://localhost:5000

### Option 2: Manual Setup
1. Install dependencies:
```bash
pip install -r requirements_web.txt
```

2. Set up your environment (create `.env` file):
```env
GROQ_API_KEY=your_groq_api_key_here
```

3. Run the web application:
```bash
python app.py
```

4. Open your browser and go to: http://localhost:5000

## 📁 File Structure

```
KPI_GPT_RAG/
├── app.py                  # Flask web application
├── templates/
│   └── index.html         # Main UI template
├── static/
│   ├── css/
│   │   └── styles.css     # Modern black theme styles
│   └── js/
│       └── main.js        # Interactive chat functionality
├── run_web_ui.py          # Easy launcher script
├── requirements_web.txt   # Web UI dependencies
└── README_WEB_UI.md      # This file
```

## 🎨 Interface Components

### Chat Interface
- **Welcome Screen**: Introduces KPI GPT with feature highlights
- **Message Bubbles**: Distinct styling for user and AI messages
- **Typing Indicator**: Shows when AI is processing your query
- **Source Citations**: Displays relevant document sources
- **Character Counter**: Real-time input validation

### Sidebar Features
- **System Status**: Live system health monitoring
- **Example Questions**: Quick-start query suggestions
- **System Information**: Database stats and model details
- **Settings Panel**: Customize your experience

### Header & Controls
- **Menu Toggle**: Responsive sidebar navigation
- **Clear Chat**: Reset conversation history
- **Settings**: Access configuration options

## ⚙️ Configuration

### Environment Variables (`.env`)
```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (with defaults)
DATA_FILE=kpi_data.txt
VECTOR_DB_PATH=./vector_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
GROQ_MODEL=llama3-8b-8192
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_RETRIEVAL_RESULTS=5
```

### User Settings (Stored in Browser)
- **Dark Mode**: Toggle between dark and light themes
- **Streaming Mode**: Enable real-time response streaming
- **Sound Effects**: Audio feedback for interactions

## 🛠️ Technical Details

### Backend
- **Flask 3.0+**: Modern Python web framework
- **RESTful API**: Clean API endpoints for chat functionality
- **Async Support**: Non-blocking request handling
- **Error Handling**: Comprehensive error management

### Frontend
- **Vanilla JavaScript**: No heavy frameworks, pure performance
- **CSS3**: Modern styling with CSS Grid, Flexbox, and animations
- **Responsive Design**: Mobile-first approach
- **Web APIs**: Local storage, notifications, and audio

### Integration
- **Seamless RAG Integration**: Uses your existing KPI GPT system
- **Real-time Status**: Live system monitoring
- **Source Attribution**: Displays document sources for transparency

## 📱 Mobile Support

The interface is fully responsive and optimized for:
- **📱 Mobile Phones**: Touch-friendly interface with optimized layouts
- **📱 Tablets**: Balanced desktop/mobile experience
- **💻 Desktop**: Full-featured interface with sidebar navigation

## 🎯 Usage Examples

### Example Queries
- "Who is the principal of KPI?"
- "Tell me about the Computer Science department"
- "What subjects are in Civil Technology 1st semester?"
- "List all departments in KPI"
- "Who is Famim Farhaz?"

### API Endpoints
- `GET /`: Main chat interface
- `POST /api/chat`: Send chat messages
- `GET /api/system/status`: Check system status
- `GET /api/examples`: Get example questions
- `POST /api/system/reset`: Reset system database

## 🔧 Troubleshooting

### Common Issues

**1. Dependencies Missing**
```bash
pip install -r requirements_web.txt
```

**2. Port Already in Use**
The app runs on port 5000 by default. Stop other applications using this port or modify the port in `app.py`.

**3. System Not Ready**
Make sure your `kpi_data.txt` file exists and contains your KPI data.

**4. API Key Issues**
Verify your Groq API key is correctly set in the `.env` file.

### Debug Mode
To enable debug mode, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🚀 Deployment

### Local Development
```bash
python run_web_ui.py
```

### Production Deployment
For production, consider using:
- **Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- **Docker**: Container deployment
- **Cloud Platforms**: Heroku, AWS, Google Cloud, etc.

## 🎨 Customization

### Themes
The CSS uses CSS custom properties (variables) for easy theming. Modify the `:root` section in `styles.css`:

```css
:root {
    --primary-bg: #0a0a0a;
    --accent-primary: #00d4aa;
    /* ... other variables */
}
```

### Adding Features
The modular JavaScript architecture makes it easy to add new features:
1. Add new methods to the `KPIGPT` class
2. Create corresponding Flask API endpoints
3. Update the UI as needed

## 📝 License

This web interface is part of the KPI GPT project created by **Famim Farhaz** for Khulna Polytechnic Institute.

## 🤝 Support

If you encounter any issues or need help:
1. Check this README first
2. Look at the browser console for JavaScript errors
3. Check the Flask logs for backend issues
4. Ensure all dependencies are properly installed

---

## 🎉 Enjoy Your Modern KPI GPT Interface!

Your KPI GPT system now has a beautiful, modern web interface that's perfect for local use. The black theme provides a professional look while the responsive design ensures it works great on any device.

**Created with ❤️ by Famim Farhaz for Khulna Polytechnic Institute** 🎓
