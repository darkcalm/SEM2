import os
import json
import requests
import time
import argparse

def download_papers(input_file, output_dir):
    """
    Downloads PDFs for papers listed in a JSON file, using their DOIs.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r') as f:
        data = json.load(f)

    for theme, papers in data.items():
        for paper in papers:
            doi = paper.get('doi')
            if not doi:
                continue

            safe_title = "".join([c for c in paper['title'] if c.isalnum() or c.isspace()]).rstrip()
            pdf_path = os.path.join(output_dir, f"{safe_title}.pdf")

            if os.path.exists(pdf_path):
                print(f"Skipping existing file: {pdf_path}")
                continue
            
            url = f"https://dx.doi.org/{doi}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            try:
                print(f"Attempting to download from: {url}")
                response = requests.get(url, headers=headers, allow_redirects=True, timeout=30)
                
                if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
                    with open(pdf_path, 'wb') as f_pdf:
                        f_pdf.write(response.content)
                    print(f"Successfully downloaded: {pdf_path}")
                else:
                    print(f"Failed to download PDF for DOI {doi}. Status: {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
                
                time.sleep(1) # Be respectful to the server
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download papers from a search results file.")
    parser.add_argument("input_file", help="Path to the JSON file of search results.")
    parser.add_argument("output_dir", help="Directory to save the downloaded PDFs.")
    
    args = parser.parse_args()
    
    download_papers(args.input_file, args.output_dir) 