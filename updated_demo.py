"""
Updated Demo Script for KPI GPT RAG System
Created by: Famim Farhaz

This script demonstrates the enhanced capabilities of the KPI GPT RAG system
including the new comprehensive curriculum data for all departments.
"""

from kpi_gpt_rag import create_kpi_rag_system
import time

def run_enhanced_demo():
    """Run enhanced demonstration of KPI GPT RAG system with curriculum data"""
    
    print("=" * 70)
    print("🎯 KPI GPT RAG System - Enhanced Demo with Curriculum Data")
    print("Created by: Famim Farhaz")
    print("=" * 70)
    
    # Initialize the RAG system
    print("\n🚀 Initializing KPI GPT RAG System...")
    try:
        rag_system = create_kpi_rag_system()
        
        print("📚 Setting up system components...")
        setup_success = rag_system.setup_system()
        
        if not setup_success:
            print("❌ Failed to setup RAG system")
            return
        
        system_info = rag_system.get_system_info()
        print(f"✅ System ready with {system_info['database']['document_count']} document chunks!\n")
        
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return
    
    # Enhanced sample queries including curriculum data
    enhanced_queries = [
        # Basic institutional queries
        "Who is the principal of KPI?",
        "What is CODE KPI?", 
        "Who is Famim Farhaz?",
        
        # Department and staff queries
        "Who is the head of Computer Science department?",
        "Tell me about Susmita Kundu",
        "List all departments in KPI",
        
        # NEW: Curriculum queries
        "What subjects are in Civil Technology 1st semester?",
        "List the subjects for Mechanical Technology 3rd semester",
        "What is subject code 26671 about?",
        "Give me the curriculum for Electronics Technology 5th semester",
        "What subjects are taught in Computer Science & Technology 7th semester?",
        "Tell me about RAC Technology curriculum",
        
        # General queries
        "What clubs are available at KPI?",
        "How many students study at KPI?"
    ]
    
    print("🔍 Running enhanced demo queries...")
    print("=" * 70)
    
    for i, query in enumerate(enhanced_queries, 1):
        print(f"\n📋 Query {i}: {query}")
        print("-" * 60)
        
        try:
            # Process the query
            response = rag_system.query(query)
            
            if 'error' not in response:
                # Show response with appropriate truncation
                answer = response['answer']
                if len(answer) > 400:
                    answer = answer[:400] + "... [truncated for demo]"
                
                print(f"🤖 Answer: {answer}")
                
                # Show top sources
                if response.get('sources'):
                    print(f"\n📚 Top sources ({min(2, len(response['sources']))}):")
                    for j, source in enumerate(response['sources'][:2], 1):
                        section = source['section']
                        score = source['similarity_score']
                        print(f"   {j}. {section} (Similarity: {score:.2f})")
            else:
                print(f"❌ Error: {response['error']}")
            
            print(f"\n📊 Model: {response.get('model_used', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
        
        # Small delay between queries
        time.sleep(0.5)
        
        if i < len(enhanced_queries):
            print("\n" + "=" * 70)
    
    # Show enhanced system statistics
    print(f"\n\n🔧 Enhanced System Information:")
    print("-" * 40)
    system_info = rag_system.get_system_info()
    
    if system_info.get('status') == 'ready':
        print(f"📊 Document chunks: {system_info['database']['document_count']}")
        print(f"🤖 Embedding model: {system_info['models']['embedding']}")
        print(f"🧠 Generation model: {system_info['models']['generation']}")
        print(f"⚙️  Chunk size: {system_info['config']['chunk_size']}")
        print(f"🔗 Max retrieval: {system_info['config']['max_retrieval_results']}")
        
        # Calculate increase in data
        old_chunks = 63
        new_chunks = system_info['database']['document_count']
        increase = ((new_chunks - old_chunks) / old_chunks) * 100
        print(f"📈 Data increase: {increase:.1f}% more content!")
        
    else:
        print(f"Status: {system_info.get('status', 'unknown')}")
    
    # New features highlight
    print(f"\n🆕 New Features Highlighted:")
    print("-" * 40)
    print("✅ Complete curriculum data for all 7 departments")
    print("✅ Subject codes and names for all 8 semesters")
    print("✅ Comprehensive booklist information")
    print("✅ Enhanced search across 78+ document chunks")
    print("✅ Improved accuracy for academic queries")
    
    print(f"\n{'=' * 70}")
    print("✨ Enhanced demo completed! The KPI GPT RAG system now includes:")
    print("   📚 Complete curriculum data for all departments")
    print("   🔍 Advanced search across institutional and academic content")
    print("   🎯 Comprehensive subject and course information")
    print("💡 You can now ask about specific subjects, semesters, and course codes!")
    print("📝 Created by: Famim Farhaz for Khulna Polytechnic Institute")
    print("=" * 70)

def interactive_curriculum_demo():
    """Interactive demo focusing on curriculum queries"""
    print("\n" + "=" * 50)
    print("🎓 Interactive Curriculum Demo")
    print("=" * 50)
    
    rag_system = create_kpi_rag_system()
    rag_system.setup_system()
    
    curriculum_examples = [
        "What subjects are in Civil 1st semester?",
        "List Electrical Technology 4th semester subjects",
        "What is 26671 Digital Marketing Technique?",
        "Show me Computer Science 6th semester curriculum",
        "What departments offer Mathematics-III?",
    ]
    
    print("\n🔍 Try these curriculum-specific queries:")
    for i, example in enumerate(curriculum_examples, 1):
        print(f"   {i}. {example}")
    
    print("\n💡 Or ask your own curriculum question!")
    print("📝 Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("🎓 Your curriculum question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for trying the curriculum demo!")
                break
            elif not user_input:
                continue
            
            print("🤖 KPI GPT:", end=" ", flush=True)
            response = rag_system.query(user_input)
            
            if 'error' not in response:
                print(response['answer'])
                if response.get('sources'):
                    print(f"\n📚 Sources: {len(response['sources'])} relevant documents found")
            else:
                print(f"❌ Error: {response['error']}")
            
            print("\n" + "-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Thanks for trying the curriculum demo!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Run the main demo
    run_enhanced_demo()
    
    # Ask if user wants interactive demo
    try:
        choice = input("\n🤔 Would you like to try the interactive curriculum demo? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_curriculum_demo()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except:
        pass
