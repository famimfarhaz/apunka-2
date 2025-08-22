"""
KPI GPT Streamlit Application
Created by: Famim Farhaz

Streamlit web application for the KPI GPT RAG system.
"""

import streamlit as st
import time
import logging
from kpi_gpt_rag import create_kpi_rag_system

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="KPI GPT - Intelligent Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2a5298;
    }
    
    .user-message {
        background-color: #f0f2f6;
        margin-left: 2rem;
    }
    
    .bot-message {
        background-color: #e8f4fd;
        margin-right: 2rem;
    }
    
    .example-button {
        background-color: #f0f2f6;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid #ddd;
        margin: 0.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .example-button:hover {
        background-color: #2a5298;
        color: white;
    }
    
    .status-good {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-loading {
        color: #ffc107;
        font-weight: bold;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    
    .stButton > button {
        background-color: #2a5298;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
    }
    
    .stButton > button:hover {
        background-color: #1e3c72;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
    st.session_state.system_ready = False
    st.session_state.messages = []
    st.session_state.system_info = {}

def initialize_rag_system():
    """Initialize the RAG system with proper error handling"""
    try:
        with st.spinner("🚀 Initializing KPI GPT RAG system..."):
            logger.info("Initializing KPI GPT RAG system...")
            rag_system = create_kpi_rag_system()
            
            logger.info("Setting up system components...")
            setup_success = rag_system.setup_system()
            
            if not setup_success:
                logger.error("Failed to setup RAG system")
                return None, "Failed to setup RAG system"
            
            logger.info("RAG system initialized successfully!")
            return rag_system, "System initialized successfully!"
            
    except Exception as e:
        logger.error(f"Error initializing RAG system: {e}")
        return None, f"Error initializing RAG system: {e}"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 KPI GPT - Intelligent Knowledge Assistant</h1>
        <p>Ask me anything about Khulna Polytechnic Institute!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150/2a5298/ffffff?text=KPI", width=150)
        st.title("🎓 KPI GPT")
        st.markdown("---")
        
        # System Status
        st.subheader("📊 System Status")
        
        if not st.session_state.system_ready:
            if st.session_state.rag_system is None:
                st.markdown('<p class="status-loading">🔄 Initializing...</p>', unsafe_allow_html=True)
                
                # Initialize system
                rag_system, message = initialize_rag_system()
                if rag_system:
                    st.session_state.rag_system = rag_system
                    st.session_state.system_ready = True
                    st.session_state.system_info = rag_system.get_system_info()
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.markdown('<p class="status-good">✅ System Ready</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-good">✅ System Ready</p>', unsafe_allow_html=True)
            
            # System Information
            if st.session_state.system_info:
                info = st.session_state.system_info
                st.write("**Database Info:**")
                if 'database' in info:
                    st.write(f"- Documents: {info['database'].get('document_count', 'N/A')}")
                    st.write(f"- Sections: {info['database'].get('section_count', 'N/A')}")
                
                st.write("**Models:**")
                if 'models' in info:
                    st.write(f"- Generation: {info['models'].get('generation', 'N/A')}")
                    st.write(f"- Embedding: {info['models'].get('embedding', 'N/A')}")
        
        st.markdown("---")
        
        # Example Questions
        st.subheader("💡 Example Questions")
        examples = [
            "Who is the principal of KPI?",
            "Tell me about the Computer Science department",
            "What is CODE KPI?",
            "What subjects are in Civil Technology 1st semester?",
            "List the departments in KPI",
            "What clubs are available at KPI?",
            "Who is Famim Farhaz?",
            "Tell me about Khulna Polytechnic Institute"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{hash(example)}", use_container_width=True):
                st.session_state.current_question = example
        
        st.markdown("---")
        
        # Reset Database
        if st.button("🔄 Reset Database", use_container_width=True):
            if st.session_state.rag_system:
                with st.spinner("Resetting database..."):
                    success = st.session_state.rag_system.reset_database()
                    if success:
                        st.success("Database reset successfully!")
                        st.session_state.system_info = st.session_state.rag_system.get_system_info()
                    else:
                        st.error("Failed to reset database")
        
        # Clear Chat
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Created by:** Famim Farhaz")
        st.markdown("**Institution:** Khulna Polytechnic Institute")
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat messages
        chat_container = st.container()
        
        with chat_container:
            if not st.session_state.messages:
                st.markdown("""
                <div class="chat-message bot-message">
                    <strong>🤖 KPI GPT:</strong><br>
                    Hello! I'm KPI GPT, your intelligent assistant for Khulna Polytechnic Institute. 
                    I can help you with information about departments, faculty, courses, facilities, and much more!
                    <br><br>
                    Feel free to ask me anything about KPI or click on the example questions in the sidebar.
                </div>
                """, unsafe_allow_html=True)
            
            # Display chat messages
            for message in st.session_state.messages:
                if message['sender'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>👤 You:</strong><br>
                        {message['text']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    sources_html = ""
                    if message.get('sources'):
                        sources_html = "<br><br><strong>📚 Sources:</strong><br>"
                        for source in message['sources'][:3]:
                            sources_html += f"• {source.get('section', 'Unknown')} (Score: {source.get('similarity_score', 0):.2f})<br>"
                    
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>🤖 KPI GPT:</strong><br>
                        {message['text']}
                        {sources_html}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        st.markdown("---")
        
        # Check for example question from sidebar
        user_input = ""
        if 'current_question' in st.session_state:
            user_input = st.session_state.current_question
            del st.session_state.current_question
        
        # Input form
        with st.form(key='chat_form', clear_on_submit=True):
            user_question = st.text_area(
                "Ask your question:",
                value=user_input,
                placeholder="Type your question about KPI here...",
                height=100,
                key="user_input"
            )
            
            col_send, col_space = st.columns([1, 3])
            with col_send:
                submit_button = st.form_submit_button("Send 📤", use_container_width=True)
        
        # Process user input
        if submit_button and user_question.strip():
            if not st.session_state.system_ready:
                st.error("⚠️ System is not ready yet. Please wait for initialization to complete.")
            else:
                # Add user message
                st.session_state.messages.append({
                    'sender': 'user',
                    'text': user_question.strip()
                })
                
                # Get AI response
                with st.spinner("🤔 Thinking..."):
                    try:
                        response = st.session_state.rag_system.query(user_question.strip())
                        
                        if 'error' in response:
                            st.session_state.messages.append({
                                'sender': 'bot',
                                'text': f"Sorry, I encountered an error: {response['error']}",
                                'sources': []
                            })
                        else:
                            st.session_state.messages.append({
                                'sender': 'bot',
                                'text': response['answer'],
                                'sources': response.get('sources', [])
                            })
                    
                    except Exception as e:
                        st.session_state.messages.append({
                            'sender': 'bot',
                            'text': f"Sorry, I encountered an unexpected error: {str(e)}",
                            'sources': []
                        })
                
                st.rerun()

if __name__ == "__main__":
    main()
