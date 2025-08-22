"""
KPI GPT Web Interface
Created by: Famim Farhaz

Flask web application providing a modern UI for the KPI GPT RAG system.
"""

from flask import Flask, render_template, request, jsonify, Response
import json
import time
import logging
from threading import Lock
from kpi_gpt_rag import create_kpi_rag_system

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

def initialize_rag_system():
    """Initialize the RAG system with proper error handling"""
    global rag_system
    
    with system_lock:
        if rag_system is None:
            try:
                logger.info("Initializing KPI GPT RAG system...")
                rag_system = create_kpi_rag_system()
                
                logger.info("Setting up system components...")
                setup_success = rag_system.setup_system()
                
                if not setup_success:
                    logger.error("Failed to setup RAG system")
                    return False
                
                logger.info("RAG system initialized successfully!")
                return True
                
            except Exception as e:
                logger.error(f"Error initializing RAG system: {e}")
                return False
    
    return True

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/api/system/status')
def system_status():
    """Get system status and information"""
    try:
        if rag_system is None:
            return jsonify({
                'status': 'not_initialized',
                'message': 'System is initializing...'
            })
        
        system_info = rag_system.get_system_info()
        return jsonify({
            'status': 'ready',
            'info': system_info,
            'message': 'System is ready!'
        })
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
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

# Initialize system on startup - using modern Flask approach
def startup():
    """Initialize RAG system on startup"""
    logger.info("Starting KPI GPT Web Interface...")
    return initialize_rag_system()

if __name__ == '__main__':
    print("🚀 Starting KPI GPT Web Interface...")
    print("=" * 50)
    
    # Initialize system
    if initialize_rag_system():
        print("✅ KPI GPT system initialized successfully!")
        print("🌐 Starting web server...")
        print("📱 Access your KPI GPT at: http://localhost:5000")
        print("=" * 50)
        
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000,
            threaded=True
        )
    else:
        print("❌ Failed to initialize KPI GPT system")
        print("Please check your configuration and try again.")
