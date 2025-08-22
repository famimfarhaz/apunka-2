#!/usr/bin/env python3

print("🔍 Checking for Julekha in kpi_data.txt...")

# Read raw file
with open('kpi_data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Total file size: {len(content)} characters")

# Search for Julekha variations
search_terms = ['Julekha', 'julekha', 'JULEKHA', 'Koli', 'koli', 'KOLI']

for term in search_terms:
    count = content.count(term)
    print(f"'{term}' found: {count} times")
    
    if count > 0:
        # Find positions and show context
        pos = content.find(term)
        while pos != -1:
            start = max(0, pos - 50)
            end = min(len(content), pos + 200)
            context = content[start:end].replace('\n', ' ')
            print(f"  Position {pos}: ...{context}...")
            pos = content.find(term, pos + 1)

print("\n" + "="*60)

# Check processed chunks using KPIDataProcessor
from data_preprocessor import KPIDataProcessor

processor = KPIDataProcessor()
clean_content = processor.clean_text(content)
chunks = processor.create_chunks(clean_content)

print(f"\nProcessed into {len(chunks)} chunks")

julekha_chunks = []
for i, chunk in enumerate(chunks):
    chunk_content = chunk['content'].lower()
    if 'julekha' in chunk_content or 'koli' in chunk_content:
        julekha_chunks.append((i, chunk))

print(f"Chunks containing Julekha/Koli: {len(julekha_chunks)}")

for i, (chunk_idx, chunk) in enumerate(julekha_chunks):
    print(f"\n--- Chunk {chunk_idx} (Section: {chunk['section']}) ---")
    print(chunk['content'][:400])
    print("..." if len(chunk['content']) > 400 else "")
