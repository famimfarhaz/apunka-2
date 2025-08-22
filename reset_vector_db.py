#!/usr/bin/env python3

import os
import shutil
from kpi_gpt_rag import create_kpi_rag_system

print("🔄 Resetting and regenerating vector database...")

# Step 1: Remove existing vector database
vector_db_path = "./vector_db"
if os.path.exists(vector_db_path):
    print(f"🗑️  Removing existing database: {vector_db_path}")
    shutil.rmtree(vector_db_path)
    print("✅ Old database removed")
else:
    print("ℹ️  No existing database found")

# Step 2: Create fresh RAG system
print("\n🆕 Creating fresh RAG system...")
rag_system = create_kpi_rag_system()

# Step 3: Setup system (this will recreate the database)
print("⚙️  Setting up system (recreating database)...")
success = rag_system.setup_system()

if success:
    print("✅ System setup successful!")
    
    # Step 4: Test search
    print("\n🧪 Testing Julekha Akter Koli search...")
    response = rag_system.query("Who is Julekha Akter Koli?")
    print(f"Response: {response['answer'][:200]}...")
    
    print(f"\n📊 Sources found: {len(response.get('sources', []))}")
    for i, source in enumerate(response.get('sources', [])[:3]):
        print(f"  {i+1}. Score: {source['similarity_score']:.3f}")
        print(f"     Content: {source['content_preview'][:100]}...")
        
else:
    print("❌ System setup failed!")
