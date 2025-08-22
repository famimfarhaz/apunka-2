"""
Simple KPI GPT Streamlit Application
Created by: Famim Farhaz

A simplified version that works reliably on Streamlit Cloud
"""

import streamlit as st
import os
import json
import time
from groq import Groq

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
        border-left-color: #28a745;
    }
    
    .bot-message {
        background-color: #e8f4fd;
        margin-right: 2rem;
        border-left-color: #2a5298;
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
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #1e3c72;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# KPI Data (embedded for simplicity)
KPI_DATA = """
About Khulna Polytechnic Institute (KPI):
Khulna Polytechnic Institute is a government technical educational institution located in Khulna, Bangladesh. It was established in 1962 and offers diploma programs in various engineering and technology fields.

Principal: Md. Abdur Razzak
Contact: 041-720751
Email: principal@kpi.edu.bd

Departments:
1. Civil Technology
2. Computer Technology
3. Electronics Technology
4. Electrical Technology
5. Mechanical Technology
6. Architecture Technology
7. Automobile Technology
8. Air Conditioning and Refrigeration Technology

Student Information:
- Famim Farhaz: Student of Civil Technology, 1st Semester, 2nd Shift, Group C
- Contact: 01843728903
- Email: famimfarhaz@gmail.com
- Facebook: facebook.com/famimfarhaz
- Creator of KPI GPT system

Facilities:
- Modern laboratories
- Computer labs
- Library
- Workshops
- Hostels
- Sports facilities

Contact Information:
Address: Khulna Polytechnic Institute, Khulna-9100, Bangladesh
Phone: 041-720751
Website: www.kpi.edu.bd
"""

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'groq_client' not in st.session_state:
    st.session_state.groq_client = None

def initialize_groq():
    """Initialize Groq client"""
    try:
        api_key = os.getenv('GROQ_API_KEY') or st.secrets.get('GROQ_API_KEY', '')
        if not api_key:
            return None, "Groq API key not found"
        
        client = Groq(api_key=api_key)
        return client, "Groq client initialized successfully"
    except Exception as e:
        return None, f"Error initializing Groq: {str(e)}"

def get_response(question, context=KPI_DATA):
    """Get response from Groq API"""
    try:
        if not st.session_state.groq_client:
            client, message = initialize_groq()
            if not client:
                return f"Error: {message}"
            st.session_state.groq_client = client
        
        # Create prompt
        prompt = f"""You are KPI GPT, an intelligent assistant for Khulna Polytechnic Institute (KPI). 
Based on the following information about KPI, answer the user's question accurately and helpfully.

KPI Information:
{context}

User Question: {question}

Please provide a helpful and accurate response. If the question is about something not covered in the KPI information, politely let the user know and suggest they ask about topics related to KPI (departments, faculty, courses, facilities, etc.).

Response:"""

        # Get response from Groq
        chat_completion = st.session_state.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

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
        
        # Check Groq API
        if not st.session_state.groq_client:
            client, message = initialize_groq()
            if client:
                st.session_state.groq_client = client
                st.markdown('<p class="status-good">✅ System Ready</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="status-error">❌ API Key Required</p>', unsafe_allow_html=True)
                st.error("Please configure your Groq API key in secrets")
        else:
            st.markdown('<p class="status-good">✅ System Ready</p>', unsafe_allow_html=True)
        
        st.markdown("**Model:** Llama 3 8B")
        st.markdown("**Provider:** Groq")
        
        st.markdown("---")
        
        # Example Questions
        st.subheader("💡 Example Questions")
        examples = [
            "Who is the principal of KPI?",
            "Tell me about the Computer Technology department",
            "What departments are available at KPI?",
            "Who is Famim Farhaz?",
            "What are the contact details of KPI?",
            "Tell me about KPI facilities",
            "What is the address of KPI?",
            "When was KPI established?"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{hash(example)}", use_container_width=True):
                st.session_state.current_question = example
        
        st.markdown("---")
        
        # Clear Chat
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Created by:** Famim Farhaz")
        st.markdown("**Institution:** Khulna Polytechnic Institute")
        st.markdown("**Department:** Civil Technology")
    
    # Main chat area
    # Chat messages container
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
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 KPI GPT:</strong><br>
                    {message['text']}
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
        if not st.session_state.groq_client:
            st.error("⚠️ System is not ready. Please check your API key configuration.")
        else:
            # Add user message
            st.session_state.messages.append({
                'sender': 'user',
                'text': user_question.strip()
            })
            
            # Get AI response
            with st.spinner("🤔 Thinking..."):
                response = get_response(user_question.strip())
                
                st.session_state.messages.append({
                    'sender': 'bot',
                    'text': response
                })
            
            st.rerun()

if __name__ == "__main__":
    main()
