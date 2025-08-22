"""
KPI GPT Web Interface
Created by: Famim Farhaz

Flask web application providing a modern UI for the KPI GPT RAG system.
"""

from flask import Flask, render_template, request, jsonify, Response
import json
import time
import logging
from threading import Lock, Thread
from kpi_gpt_rag import create_kpi_rag_system
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kpi-gpt-secret-key-2024'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# Global RAG system instance
rag_system = None
system_lock = Lock()
initialization_status = {
    'status': 'starting',
    'message': 'System is starting up...',
    'progress': 0,
    'error': None
}

def initialize_rag_system_background():
    """Initialize the RAG system in background with progress tracking"""
    global rag_system, initialization_status
    
    try:
        with system_lock:
            if rag_system is not None:
                return True
                
            # Update status: Creating system
            initialization_status.update({
                'status': 'initializing',
                'message': 'Creating RAG system...',
                'progress': 20
            })
            
            logger.info("Initializing KPI GPT RAG system...")
            rag_system = create_kpi_rag_system()
            
            # Update status: Setting up components
            initialization_status.update({
                'status': 'initializing',
                'message': 'Setting up system components...',
                'progress': 40
            })
            
            logger.info("Setting up system components...")
            setup_success = rag_system.setup_system()
            
            if not setup_success:
                initialization_status.update({
                    'status': 'error',
                    'message': 'Failed to setup RAG system',
                    'progress': 0,
                    'error': 'Setup failed'
                })
                logger.error("Failed to setup RAG system")
                rag_system = None
                return False
            
            # Update status: Ready
            initialization_status.update({
                'status': 'ready',
                'message': 'System is ready!',
                'progress': 100,
                'error': None
            })
            
            logger.info("RAG system initialized successfully!")
            return True
            
    except Exception as e:
        initialization_status.update({
            'status': 'error',
            'message': f'Initialization failed: {str(e)}',
            'progress': 0,
            'error': str(e)
        })
        logger.error(f"Error initializing RAG system: {e}")
        rag_system = None
        return False

def initialize_rag_system():
    """Initialize the RAG system with proper error handling - Legacy function"""
    return initialize_rag_system_background()

def startup():
    """Legacy startup function for backwards compatibility"""
    logger.info("Legacy startup function called")
    return initialize_rag_system_background()

def start_background_initialization():
    """Start background initialization in a separate thread"""
    def init_worker():
        logger.info("Starting background initialization...")
        initialize_rag_system_background()
    
    # Start initialization in background thread
    init_thread = Thread(target=init_worker, daemon=True)
    init_thread.start()
    logger.info("Background initialization started")

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'service': 'KPI GPT',
        'timestamp': int(time.time())
    })

@app.route('/api/system/status')
def system_status():
    """Get system status and information"""
    try:
        # Failsafe: If system is not initialized and not currently initializing, start it
        if rag_system is None and initialization_status['status'] not in ['initializing', 'error']:
            logger.info("Failsafe: Starting background initialization from status check")
            start_background_initialization()
            
        if rag_system is None:
            return jsonify(initialization_status)
        
        system_info = rag_system.get_system_info()
        return jsonify({
            'status': 'ready',
            'info': system_info,
            'message': 'System is ready!',
            'progress': 100
        })
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}',
            'progress': 0
        })

@app.route('/api/system/initialize', methods=['POST'])
def initialize_system():
    """Manually trigger system initialization"""
    try:
        if rag_system is not None:
            return jsonify({
                'success': True,
                'message': 'System is already initialized',
                'status': 'ready'
            })
        
        # Start background initialization
        start_background_initialization()
        
        return jsonify({
            'success': True,
            'message': 'Initialization started in background',
            'status': 'initializing'
        })
        
    except Exception as e:
        logger.error(f"Error starting initialization: {e}")
        return jsonify({
            'success': False,
            'message': f'Failed to start initialization: {str(e)}',
            'status': 'error'
        })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            })
        
        if rag_system is None:
            return jsonify({
                'success': False,
                'error': 'System is not initialized yet. Please wait...'
            })
        
        # Process the query
        logger.info(f"Processing query: {user_message}")
        response = rag_system.query(user_message)
        
        if 'error' in response:
            return jsonify({
                'success': False,
                'error': response['error'],
                'query': user_message
            })
        
        return jsonify({
            'success': True,
            'query': user_message,
            'answer': response['answer'],
            'sources': response.get('sources', []),
            'model_used': response.get('model_used', 'Unknown'),
            'system_info': response.get('system_info', {})
        })
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Handle streaming chat responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return Response("No message provided", mimetype='text/plain')
        
        if rag_system is None:
            return Response("System not initialized", mimetype='text/plain')
        
        def generate_stream():
            try:
                for chunk in rag_system.stream_query(user_message):
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'done': True})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return Response(generate_stream(), mimetype='text/event-stream')
        
    except Exception as e:
        logger.error(f"Error in streaming chat: {e}")
        return Response(f"Error: {str(e)}", mimetype='text/plain')

@app.route('/api/examples')
def get_examples():
    """Get sample queries for the user"""
    examples = [
        "Who is the principal of KPI?",
        "Tell me about the Computer Science department",
        "What is CODE KPI?",
        "What subjects are in Civil Technology 1st semester?",
        "List the departments in KPI",
        "What clubs are available at KPI?",
        "Who is Famim Farhaz?",
        "Give me the curriculum for Electronics Technology 5th semester",
        "Tell me about Khulna Polytechnic Institute"
    ]
    
    return jsonify({
        'examples': examples
    })

@app.route('/api/system/reset', methods=['POST'])
def reset_system():
    """Reset the RAG system database"""
    try:
        if rag_system is None:
            return jsonify({
                'success': False,
                'message': 'System not initialized'
            })
        
        logger.info("Resetting system database...")
        success = rag_system.reset_database()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Database reset successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to reset database'
            })
            
    except Exception as e:
        logger.error(f"Error resetting system: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

# Flask startup hook - Removed for Flask 3.0 compatibility
# @app.before_first_request was deprecated and removed in Flask 3.0
# Background initialization now handled in production startup section

# Production startup
def create_app():
    """Create Flask app for production deployment"""
    logger.info("Creating Flask app for production...")
    
    # Start background initialization immediately
    start_background_initialization()
    
    return app

# For production servers (like Render)
# Initialize when imported by WSGI servers like gunicorn
# This ensures the system starts up regardless of how the module is loaded
try:
    # Check if we're being imported by a WSGI server
    if __name__ != '__main__' or 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
        logger.info("Starting KPI GPT in production mode...")
        start_background_initialization()
except Exception as e:
    logger.error(f"Error in production startup: {e}")
    # Continue anyway, initialization will be triggered on first request

if __name__ == '__main__':
    print("🚀 Starting KPI GPT Web Interface...")
    print("=" * 50)
    
    # For local development, initialize fully first
    if os.getenv('FLASK_ENV') == 'development' or os.getenv('DEBUG') == 'true':
        print("Development mode: Full initialization...")
        if initialize_rag_system():
            print("✅ KPI GPT system initialized successfully!")
        else:
            print("❌ Failed to initialize KPI GPT system")
            print("Will start with background initialization...")
            start_background_initialization()
    else:
        print("Production mode: Background initialization...")
        start_background_initialization()
    
    print("🌐 Starting web server...")
    print("📱 Access your KPI GPT at: http://localhost:5000")
    print("=" * 50)
    
    app.run(
        debug=False,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 10000)),  # Render default port
        threaded=True
    )
