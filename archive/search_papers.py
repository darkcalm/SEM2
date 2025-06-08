import os
import json
import time
import argparse
from dotenv import load_dotenv
from semanticscholar import SemanticScholar

def search_papers(query_file, output_file, limit, max_retries, retry_delay):
    """
    Searches for papers using the Semantic Scholar API based on a query file.
    """
    load_dotenv()
    api_key = os.getenv("S2_API_KEY")
    if not api_key:
        raise ValueError("S2_API_KEY not found in .env file or environment.")

    s2 = SemanticScholar(api_key=api_key)
    
    with open(query_file, 'r') as f:
        queries_data = json.load(f)

    all_results = {}
    for theme, queries in queries_data.items():
        theme_results = []
        for query in queries:
            print(f"Searching for: '{query}'")
            for attempt in range(max_retries):
                try:
                    results = s2.search_paper(query, limit=limit)
                    for item in results:
                        if item.doi:
                            theme_results.append({
                                'title': item.title,
                                'authors': [author['name'] for author in item.authors],
                                'year': item.year,
                                'doi': item.doi
                            })
                    break 
                except Exception as e:
                    print(f"  Attempt {attempt + 1}/{max_retries} failed for '{query}': {e}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                    else:
                        print(f"  Failed to retrieve results for '{query}'.")
        all_results[theme] = theme_results

    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=4)
    
    print(f"Search complete. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for papers using the Semantic Scholar API.")
    parser.add_argument("query_file", help="Path to the JSON file containing search queries.")
    parser.add_argument("output_file", help="Path to save the JSON results.")
    parser.add_argument("--limit", type=int, default=5, help="Number of papers to retrieve per query.")
    parser.add_argument("--max_retries", type=int, default=3, help="Maximum number of retries per query.")
    parser.add_argument("--retry_delay", type=int, default=5, help="Delay in seconds between retries.")
    
    args = parser.parse_args()
    
    search_papers(args.query_file, args.output_file, args.limit, args.max_retries, args.retry_delay) 