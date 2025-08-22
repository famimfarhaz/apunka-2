#!/usr/bin/env python3
"""
Diagnostic script to check section pattern matching
"""

from data_preprocessor import KPIDataProcessor
import re

def diagnose_section_patterns():
    """Diagnose why section patterns aren't matching"""
    
    processor = KPIDataProcessor()
    content = processor.load_data('kpi_data.txt')
    
    # Test section patterns
    patterns = {
        'about_college': r'\*\*About College:\*\*',
        'teachers': r'\*\*List of Teachers',
        'class_captains': r'CLass Captains :',
        'creator_info': r'KPI GPT Creator'
    }
    
    print('=== Testing section patterns ===')
    for name, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        status = "FOUND" if match else "NOT FOUND"
        print(f'{name}: {status} - Pattern: {pattern}')
        if match:
            print(f'  Found at position: {match.start()}-{match.end()}')
            print(f'  Context: "{content[max(0, match.start()-20):match.end()+20]}"')
        print()
    
    print('\n=== Looking for actual section headers ===')
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ['**about', 'teacher', 'captain', 'creator', 'official']):
            print(f'Line {i+1}: "{line.strip()}"')
            
    print('\n=== Testing structured data extraction ===')
    structured_data = processor.extract_structured_data(content)
    for section_name, section_content in structured_data.items():
        print(f'{section_name}: {len(section_content)} characters')
        if section_content:
            print(f'  Preview: "{section_content[:100]}..."')
        print()

if __name__ == "__main__":
    diagnose_section_patterns()
