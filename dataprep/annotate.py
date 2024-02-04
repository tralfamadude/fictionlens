"""
Requires env to have var OPENAI_API_KEY

"""

import json
import openai
import os
import sys

def read_jsonl_file(filename):
    with open(filename, 'r') as file:
        return [json.loads(line) for line in file]

def write_jsonl_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(json.dumps(item) + '\n')

def get_embeddings(data):
    for item in data:
        response = openai.Embedding.create(input=item['text'])
        item['embedding'] = response['data'][0]['embedding']
    return data

def annotate_with_gpt4(data):
    for item in data:
        prompt = f"Your custom prompt here with {item['text']}"
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt)
        item['annotate'] = response['choices'][0]['text'].strip()
    return data

def main():
    if len(sys.argv) != 2:
        print("Usage: python annotate.py <filename.jsonl>  # which will write another file")
        sys.exit(1)
    
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print("File does not exist.")
        sys.exit(1)
    
    # Set up OpenAI key
    mykey = os.getenv("OPENAI_API_KEY")
    if len(mykey) == 0:
        print("OPENAI_API_KEY env var not found")
        sys.exit(1)
    openai.api_key = mykey
    data = read_jsonl_file(filename)
    print(f"Processing {filename} for embeddings, {len(data)} paragraphs")
    data = get_embeddings(data)
    print(f"Embeddings finished. Annotating next...")
    data = annotate_with_gpt4(data)
    
    new_filename = f"{os.path.splitext(filename)[0]}.annotated.jsonl"
    write_jsonl_file(new_filename, data)
    
    print(f"Processing complete. Data saved to {new_filename}")

if __name__ == "__main__":
    main()

