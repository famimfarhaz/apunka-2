#!/usr/bin/env python3

from data_preprocessor import DataPreprocessor

print("🔍 Searching for Julekha directly in processed data...")

# Load and process data
processor = DataPreprocessor()
data = processor.load_data("kpi_data.txt")

print(f"Total data length: {len(data)} characters")

# Search for Julekha
julekha_positions = []
for i, char in enumerate(data):
    if data[i:i+7].lower() == "julekha":
        start = max(0, i-100)
        end = min(len(data), i+500)
        context = data[start:end]
        julekha_positions.append((i, context))

print(f"\nFound {len(julekha_positions)} occurrences of 'Julekha':")

for i, (pos, context) in enumerate(julekha_positions):
    print(f"\n{i+1}. Position {pos}:")
    print(f"Context: {context}")
    print("-" * 80)

# Also check chunks
print("\n🔗 Checking processed chunks...")
chunks = processor.process_data(data)
print(f"Total chunks: {len(chunks)}")

julekha_chunks = []
for i, chunk in enumerate(chunks):
    if "julekha" in chunk.lower():
        julekha_chunks.append((i, chunk))

print(f"\nFound Julekha in {len(julekha_chunks)} chunks:")
for i, (chunk_idx, chunk) in enumerate(julekha_chunks):
    print(f"\n{i+1}. Chunk {chunk_idx}:")
    print(f"Content: {chunk[:300]}...")
    print("-" * 80)
