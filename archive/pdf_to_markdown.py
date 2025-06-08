import fitz  # PyMuPDF
import sys

def convert_pdf_to_markdown(pdf_path, markdown_path):
    """
    Converts a PDF file to a Markdown file.
    """
    try:
        doc = fitz.open(pdf_path)
        markdown_content = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            markdown_content += f"## Page {page_num + 1}\n\n"
            markdown_content += text
            markdown_content += "\n\n---\n\n"
        
        with open(markdown_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        
        print(f"Successfully converted {pdf_path} to {markdown_path}")

    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python 15.3_pdf_to_markdown.py <input_pdf> <output_markdown>")
    else:
        convert_pdf_to_markdown(sys.argv[1], sys.argv[2]) 