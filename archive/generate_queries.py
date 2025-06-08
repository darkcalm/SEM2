import json
import re
import argparse
from itertools import combinations

def generate_queries_from_source(source_file, output_file):
    """
    Analyzes a source markdown file to extract key concepts and generate
    structured search queries for academic literature APIs.
    """
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define core concepts and related keywords
    # This could be made more sophisticated with NLP topic modeling
    concept_map = {
        'ethics': ['ethic', 'ethical', 'justice', 'moral', 'responsibility', 'social acceptance'],
        'sustainability': ['sustainab', 'renewable', 'green', 'circular economy', 'sustainable development'],
        'open_science': ['open science', 'open data', 'open source', 'reproducib', 'transparen', 'FAIR data'],
        'energy_research': ['energy research', 'energy systems', 'energy transition', 'energy access', 'energy modeling']
    }
    
    found_keywords = {concept: [] for concept in concept_map}
    
    # Find all occurrences of keywords from the concept map in the source text
    for concept, keywords in concept_map.items():
        for keyword in keywords:
            # Use word boundaries to avoid matching parts of words
            if re.search(r'\b' + re.escape(keyword) + r'\b', content, re.IGNORECASE):
                # Use the base keyword for queries
                found_keywords[concept].append(keyword.split()[0]) # Take the first word for multi-word keywords
    
    # Deduplicate keywords
    for concept in found_keywords:
        found_keywords[concept] = list(set(found_keywords[concept]))

    # Generate queries by combining concepts
    generated_queries = {}
    
    # Generate queries by combining two primary concepts
    primary_concepts = ['ethics', 'sustainability', 'open_science']
    for L in range(2, 3): # Combinations of 2
        for combo in combinations(primary_concepts, L):
            theme_name = f"theme_combo_{'_'.join(combo)}"
            queries = []
            
            concept1_keywords = found_keywords[combo[0]]
            concept2_keywords = found_keywords[combo[1]]
            
            # Create queries by pairing keywords from each concept
            for kw1 in concept1_keywords:
                for kw2 in concept2_keywords:
                    # Formulate a query using exact phrases for better precision
                    queries.append(f'"{kw1}" + "{kw2}"')
            
            generated_queries[theme_name] = queries

    # Add queries combining each primary concept with "energy_research"
    for concept in primary_concepts:
        theme_name = f"theme_focus_{concept}_energy"
        queries = []
        for kw_concept in found_keywords[concept]:
            for kw_energy in found_keywords['energy_research']:
                 queries.append(f'"{kw_concept}" + "{kw_energy}"')
        generated_queries[theme_name] = queries


    with open(output_file, 'w') as f:
        json.dump(generated_queries, f, indent=4)

    print(f"Generated {sum(len(q) for q in generated_queries.values())} search queries in {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate search queries from a source document.")
    parser.add_argument("source_file", help="Path to the source markdown document (e.g., PRD, instructions).")
    parser.add_argument("output_file", help="Path to save the generated JSON queries.")
    
    args = parser.parse_args()
    
    generate_queries_from_source(args.source_file, args.output_file) 