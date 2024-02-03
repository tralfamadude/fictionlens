"""
usage: python epub_scan.py something.epub

Use no-image epub. Not sure if epub3 format will work. 

Manually remove front matter by editing the jsonl file. 
"""
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import json
import sys
import os

def epub_scan(filename):
    book = epub.read_epub(filename)
    paragraphs = []
    para_num = 1
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = p.get_text().strip()
                if len(text) > 4:  # Ensure the paragraph is not empty, not too short
                    paragraphs.append({"text": text, "id": para_num})
                    para_num += 1
    return paragraphs

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_epub_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    paragraphs = epub_scan(input_file)
    
    # Generate the output filename by changing the extension to .jsonl
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}.jsonl"
    
    with open(output_file, 'w') as f:
        for paragraph in paragraphs:
            f.write(json.dumps(paragraph) + '\n')
    
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()
