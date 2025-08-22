"""
Data Preprocessing Module for KPI GPT RAG System
Created by: Famim Farhaz

This module handles data preprocessing, chunking, and text processing
for the KPI GPT RAG system.
"""

import os
import re
from typing import List, Dict, Any
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KPIDataProcessor:
    """Processes KPI GPT data for RAG system"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def load_data(self, file_path: str) -> str:
        """Load data from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info(f"Successfully loaded data from {file_path}")
            return content
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            raise
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        # Remove line numbers at the start of lines
        text = re.sub(r'^\d+\|', '', text, flags=re.MULTILINE)
        
        # Clean up excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove any remaining artifacts
        text = text.strip()
        
        return text
    
    def extract_structured_data(self, text: str) -> Dict[str, Any]:
        """Extract structured information from the text"""
        sections = {}
        
        # Extract different sections
        sections['about_college'] = self._extract_section(text, r'\*\*About College:\*\*', r'\*\*Departments')
        sections['departments'] = self._extract_section(text, r'\*\*Departments of the Polytechnic Institute:\*\*', r'Since 2008')
        sections['department_heads'] = self._extract_section(text, r'\*\*Department Details:\*\*', r'---')
        sections['officials'] = self._extract_section(text, r'\*\*Officials:\*\*', r'\*\*List of Teachers')
        sections['teachers'] = self._extract_section(text, r'\*\*List of Teachers', r'Principal:')
        sections['principal'] = self._extract_section(text, r'Principal:', r'College Clubs')
        sections['clubs'] = self._extract_section(text, r'College Clubs at Khulna Polytechnic Institute', r'CLass Captains')
        sections['class_captains'] = self._extract_section(text, r'CLass Captains :', r'KPI GPT Creator')
        sections['creator_info'] = self._extract_section(text, r'KPI GPT Creator', r'$')
        
        return sections
    
    def _extract_section(self, text: str, start_pattern: str, end_pattern: str) -> str:
        """Extract a section of text between two patterns"""
        try:
            start_match = re.search(start_pattern, text, re.IGNORECASE)
            if not start_match:
                return ""
            
            start_pos = start_match.end()
            
            if end_pattern == '$':  # End of text
                return text[start_pos:].strip()
            
            end_match = re.search(end_pattern, text[start_pos:], re.IGNORECASE)
            if not end_match:
                return text[start_pos:].strip()
            
            end_pos = start_pos + end_match.start()
            return text[start_pos:end_pos].strip()
        except Exception as e:
            logger.warning(f"Error extracting section {start_pattern}: {e}")
            return ""
    
    def create_chunks(self, text: str) -> List[Dict[str, Any]]:
        """Create overlapping chunks from text"""
        chunks = []
        
        # First, try to create semantic chunks based on structure
        structured_data = self.extract_structured_data(text)
        
        for section_name, section_content in structured_data.items():
            if section_content:
                section_chunks = self._create_section_chunks(
                    section_content, section_name
                )
                chunks.extend(section_chunks)
        
        # If structured chunking doesn't work well, fall back to size-based chunking
        if len(chunks) < 5:
            logger.info("Using size-based chunking as fallback")
            chunks = self._create_size_based_chunks(text)
        
        return chunks
    
    def _create_section_chunks(self, text: str, section_name: str) -> List[Dict[str, Any]]:
        """Create chunks for a specific section"""
        chunks = []
        
        if len(text) <= self.chunk_size:
            chunks.append({
                'content': text,
                'section': section_name,
                'chunk_id': f"{section_name}_0",
                'metadata': {
                    'section': section_name,
                    'length': len(text)
                }
            })
        else:
            # Split large sections into smaller chunks
            words = text.split()
            current_chunk = []
            current_length = 0
            chunk_num = 0
            
            for word in words:
                word_length = len(word) + 1  # +1 for space
                
                if current_length + word_length > self.chunk_size and current_chunk:
                    chunks.append({
                        'content': ' '.join(current_chunk),
                        'section': section_name,
                        'chunk_id': f"{section_name}_{chunk_num}",
                        'metadata': {
                            'section': section_name,
                            'length': current_length,
                            'chunk_num': chunk_num
                        }
                    })
                    
                    # Create overlap
                    overlap_words = current_chunk[-self.chunk_overlap//10:] if len(current_chunk) > self.chunk_overlap//10 else current_chunk
                    current_chunk = overlap_words + [word]
                    current_length = sum(len(w) + 1 for w in current_chunk)
                    chunk_num += 1
                else:
                    current_chunk.append(word)
                    current_length += word_length
            
            # Add the last chunk
            if current_chunk:
                chunks.append({
                    'content': ' '.join(current_chunk),
                    'section': section_name,
                    'chunk_id': f"{section_name}_{chunk_num}",
                    'metadata': {
                        'section': section_name,
                        'length': current_length,
                        'chunk_num': chunk_num
                    }
                })
        
        return chunks
    
    def _create_size_based_chunks(self, text: str) -> List[Dict[str, Any]]:
        """Create chunks based on size only"""
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        chunk_num = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > self.chunk_size and current_chunk:
                chunks.append({
                    'content': ' '.join(current_chunk),
                    'section': 'general',
                    'chunk_id': f"chunk_{chunk_num}",
                    'metadata': {
                        'section': 'general',
                        'length': current_length,
                        'chunk_num': chunk_num
                    }
                })
                
                # Create overlap
                overlap_words = current_chunk[-self.chunk_overlap//10:] if len(current_chunk) > self.chunk_overlap//10 else current_chunk
                current_chunk = overlap_words + [word]
                current_length = sum(len(w) + 1 for w in current_chunk)
                chunk_num += 1
            else:
                current_chunk.append(word)
                current_length += word_length
        
        # Add the last chunk
        if current_chunk:
            chunks.append({
                'content': ' '.join(current_chunk),
                'section': 'general',
                'chunk_id': f"chunk_{chunk_num}",
                'metadata': {
                    'section': 'general',
                    'length': current_length,
                    'chunk_num': chunk_num
                }
            })
        
        return chunks
    
    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Main processing function"""
        logger.info(f"Processing file: {file_path}")
        
        # Load raw data
        raw_data = self.load_data(file_path)
        
        # Clean text
        cleaned_data = self.clean_text(raw_data)
        
        # Create chunks
        chunks = self.create_chunks(cleaned_data)
        
        logger.info(f"Created {len(chunks)} chunks from the data")
        
        return chunks

if __name__ == "__main__":
    # Test the processor
    processor = KPIDataProcessor()
    chunks = processor.process_file("kpi_data.txt")
    
    print(f"Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
        print(f"\nChunk {i+1}:")
        print(f"Section: {chunk['section']}")
        print(f"Content preview: {chunk['content'][:100]}...")
        print(f"Metadata: {chunk['metadata']}")
