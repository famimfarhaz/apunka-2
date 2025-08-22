# 🎓 KPI GPT - Intelligent Knowledge Assistant

A powerful AI-driven chatbot built specifically for Khulna Polytechnic Institute (KPI), providing instant answers to questions about the institute, departments, curriculum, faculty, and more.

## 🚀 Features

- **Smart Q&A System**: Ask questions about KPI in natural language
- **Comprehensive Knowledge Base**: Information about departments, courses, faculty, and institute details
- **Real-time Responses**: Fast and accurate answers powered by advanced AI
- **User-Friendly Interface**: Clean, modern web interface
- **Conversation Memory**: Maintains context throughout your chat session

## 💡 Example Questions

- "Who is the principal of KPI?"
- "Tell me about the Computer Science department"
- "What subjects are in Civil Technology 1st semester?"
- "What clubs are available at KPI?"
- "Give me the curriculum for Electronics Technology 5th semester"

## 🛠 Technology Stack

- **Backend**: Python Flask
- **AI Model**: Groq LLM with RAG (Retrieval Augmented Generation)
- **Vector Database**: ChromaDB
- **Text Processing**: LangChain, Sentence Transformers
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Railway/Render compatible

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/famimfarhaz/apun-ka1.git
cd apun-ka1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file and add your API keys
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the application:
```bash
python app.py
```

5. Visit `http://localhost:5000` to use KPI GPT!

## 🌐 Live Demo

[Live Demo Coming Soon]

## 📝 API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send a message to KPI GPT
- `GET /api/system/status` - Check system status
- `GET /api/examples` - Get example queries
- `POST /api/system/reset` - Reset the system database

## 👨‍💻 Developer

Created by **Famim Farhaz** - Computer Science & Technology Student at KPI

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📞 Support

If you have any questions or need support, please create an issue in this repository.

---

Made with ❤️ for Khulna Polytechnic Institute

# KPI GPT RAG System

**A Retrieval-Augmented Generation (RAG) system for Khulna Polytechnic Institute**

Created by: **Famim Farhaz**

---

## 📚 Overview

KPI GPT is an AI-powered question-answering system specifically designed for Khulna Polytechnic Institute (KPI). It uses advanced Retrieval-Augmented Generation (RAG) technology to provide accurate and contextual answers about the institute, including information about departments, teachers, staff, students, facilities, and policies.

## ✨ Features

- 🤖 **Advanced RAG Architecture**: Combines vector search with large language models
- 🔍 **Intelligent Retrieval**: Finds relevant information from KPI database
- 💬 **Natural Conversations**: Provides human-like responses about KPI
- 📊 **Real-time Information**: Access to comprehensive KPI database
- 🚀 **Fast Responses**: Optimized for quick query processing
- 🔧 **Configurable**: Easily customizable settings and parameters

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   Vector Search   │───▶│  Context Docs   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   KPI Database  │    │   ChromaDB       │    │   Groq API      │
│   (Text Data)   │───▶│  (Vector Store)  │    │  (LLM Generate) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ Final Response  │
                                                └─────────────────┘
```

## 🛠️ Components

### 1. Data Preprocessor (`data_preprocessor.py`)
- Loads and processes KPI data
- Chunks text for optimal retrieval
- Structures information by sections

### 2. Vector Database (`vector_database.py`)
- Uses ChromaDB for vector storage
- Sentence Transformers for embeddings
- Similarity search functionality

### 3. Groq Client (`groq_client.py`)
- Integrates with Groq API
- Handles text generation
- RAG prompt engineering

### 4. Main Application (`kpi_gpt_rag.py`)
- Combines all components
- User interface and query processing
- System management

### 5. Configuration (`config.py`)
- Environment variables management
- System settings and validation

## 📋 Requirements

- Python 3.8+
- Groq API Key
- Required packages (see `requirements.txt`)

## 🚀 Installation

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file with:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DB_PATH=./vector_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_RETRIEVAL_RESULTS=5
TEMPERATURE=0.7
```

4. **Prepare data:**
Ensure `kpi_data.txt` contains your KPI information

## 🎯 Usage

### Command Line Interface

```bash
python kpi_gpt_rag.py
```

### Python API

```python
from kpi_gpt_rag import create_kpi_rag_system

# Create RAG system
rag_system = create_kpi_rag_system()

# Setup system
rag_system.setup_system()

# Query the system
response = rag_system.query("Who is the principal of KPI?")
print(response['answer'])
```

### Example Queries

- "Who is the principal of KPI?"
- "Tell me about the Computer Science department"
- "What are the contact details for the Civil department head?"
- "List all the departments in KPI"
- "Who is Famim Farhaz?"

## 📊 Data Structure

The system processes KPI data organized in sections:

- **About College**: General information about KPI
- **Departments**: List of all departments
- **Department Heads**: Contact information for heads
- **Officials**: Staff and administrator details
- **Teachers**: Faculty information by department
- **Principal**: Principal's contact information
- **Clubs**: Student clubs and activities
- **Class Captains**: Student representative information
- **Creator Info**: System creator information

## ⚙️ Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `CHUNK_SIZE` | Size of text chunks for processing | 1000 |
| `CHUNK_OVERLAP` | Overlap between chunks | 200 |
| `MAX_RETRIEVAL_RESULTS` | Number of documents to retrieve | 5 |
| `TEMPERATURE` | LLM response creativity (0-1) | 0.7 |
| `EMBEDDING_MODEL` | Sentence transformer model | all-MiniLM-L6-v2 |
| `GROQ_MODEL` | Groq language model | llama-3.1-70b-versatile |

## 🧪 Testing

Run individual components:

```bash
# Test data processing
python data_preprocessor.py

# Test vector database
python vector_database.py

# Test Groq client
python groq_client.py

# Test configuration
python config.py
```

## 📁 Project Structure

```
KPI_GPT_RAG/
├── kpi_gpt_rag.py          # Main application
├── data_preprocessor.py    # Data processing module
├── vector_database.py      # Vector database operations
├── groq_client.py         # Groq API integration
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── kpi_data.txt          # KPI information data
├── README.md             # This file
└── vector_db/            # Vector database storage (auto-created)
```

## 🔧 Advanced Usage

### Rebuild Database
```python
rag_system.setup_system(rebuild_db=True)
```

### Updated Data
The system has been updated with the latest KPI data from "KPI_GPT_DATA_English - Copy.txt" which includes:
- Enhanced department information
- Updated faculty and staff details
- Current course structures and syllabi
- Club and organization information
- Latest contact information

### Test Updated System
```bash
python test_updated_system.py
```

### Streaming Responses
```python
for chunk in rag_system.stream_query("Your question"):
    print(chunk, end='', flush=True)
```

### System Information
```python
info = rag_system.get_system_info()
print(info)
```

## 📈 Performance

- **Setup Time**: ~30-60 seconds (first run)
- **Query Response**: ~2-5 seconds
- **Memory Usage**: ~500MB-1GB
- **Database Size**: ~10-50MB (depends on data)

## 🤝 Contributing

Created by **Famim Farhaz** for Khulna Polytechnic Institute.

### Student Information
- **Name**: Famim Farhaz
- **Institution**: Khulna Polytechnic Institute
- **Department**: Civil Technology
- **Semester**: 1st
- **Shift**: 2nd
- **Group**: C
- **Contact**: 01843728903
- **Email**: famimfarhaz@gmail.com
- **Facebook**: [facebook.com/famimfarhaz](https://web.facebook.com/famimfarhaz)

## 📄 License

This project is created for educational purposes at Khulna Polytechnic Institute.

## 🐛 Troubleshooting

### Common Issues

1. **"Groq API key is required"**
   - Set your Groq API key in the `.env` file
   
2. **"Data file not found"**
   - Ensure `kpi_data.txt` exists in the project directory
   
3. **"Failed to initialize database"**
   - Check if you have write permissions in the project directory
   - Try deleting the `vector_db` folder and rerunning

4. **Slow performance**
   - Reduce `CHUNK_SIZE` or `MAX_RETRIEVAL_RESULTS`
   - Use a smaller embedding model

## 📞 Support

For support or questions about this system:
- **Email**: famimfarhaz@gmail.com
- **Facebook**: [facebook.com/famimfarhaz](https://web.facebook.com/famimfarhaz)
- **Phone**: 01843728903

---

**Built with ❤️ for Khulna Polytechnic Institute by Famim Farhaz**
