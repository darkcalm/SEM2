import os
import argparse
import PyPDF2
from pathlib import Path

def convert_pdfs_to_md(input_dir, output_dir):
    """
    Converts all PDF files in a directory to markdown files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, Path(filename).with_suffix('.md').name)
            
            print(f"Converting {pdf_path} to {output_path}...")
            
            try:
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text = ""
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\\n"
                    
                    # Basic text cleaning
                    text = text.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
                    
                    with open(output_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(text)
                print(f"Successfully converted {filename}")
            except Exception as e:
                print(f"Could not convert {filename}. Reason: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert all PDFs in a directory to Markdown.")
    parser.add_argument("input_dir", help="Directory containing PDF files.")
    parser.add_argument("output_dir", help="Directory to save the Markdown files.")
    
    args = parser.parse_args()
    
    convert_pdfs_to_md(args.input_dir, args.output_dir) 