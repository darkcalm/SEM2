import os
import re
from pathlib import Path

def censor_text(text):
    # Course code patterns
    text = re.sub(r'MJ\d{4}', 'COURSE_CODE', text)
    
    # Course-related terms
    course_terms = [
        r'Seminar\s+\d+',
        r'Lecture\s+\d+',
        r'Instructions_\d{4}',
        r'Open\s+Science',
        r'Energy\s+Research',
        r'Practice\s+Lecture'
    ]
    
    for term in course_terms:
        text = re.sub(term, 'COURSE_TERM', text, flags=re.IGNORECASE)
    
    # Date patterns in format YYYY-MM-DD or similar
    text = re.sub(r'\d{4}-\d{2}-\d{2}', 'DATE', text)
    
    return text

def censor_filename(filename):
    # Remove course codes
    filename = re.sub(r'MJ\d{4}', 'COURSE', filename)
    
    # Remove specific course-related terms
    filename = re.sub(r'Seminar\s+\d+', 'Seminar', filename)
    filename = re.sub(r'Lecture\s+\d+', 'Lecture', filename)
    filename = re.sub(r'Instructions_\d{4}', 'Instructions', filename)
    filename = re.sub(r'Open\s+Science', 'Topic', filename)
    filename = re.sub(r'Energy\s+Research', 'Research', filename)
    filename = re.sub(r'Practice\s+Lecture', 'Lecture', filename)
    
    # Remove dates
    filename = re.sub(r'\d{4}-\d{2}-\d{2}', '', filename)
    filename = re.sub(r'_\d{4}', '', filename)
    
    # Clean up any double spaces or underscores
    filename = re.sub(r'\s+', ' ', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip(' _-')
    
    return filename

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            
            # Read and censor content
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            censored_content = censor_text(content)
            
            # Create new filename
            new_filename = censor_filename(filename)
            output_path = os.path.join(output_dir, new_filename)
            
            # Write censored content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(censored_content)
            
            print(f"Processed: {filename} -> {new_filename}")

if __name__ == "__main__":
    input_dir = "external/markdown"
    output_dir = "external/censored"
    process_directory(input_dir, output_dir) 