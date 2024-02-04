"""
Requires env to have var OPENAI_API_KEY

"""

import json
from openai import OpenAI

import os
import sys

annotation_prompt="""
In the text quoted below, determine the sentiment as -1,0,1 for bad, neutral, good. Identify the names of persons or places. Format these into a JSON with the keys "sentiment" and "entities". Only give JSON as the response. 
"""

# Set up OpenAI key
mykey = os.getenv("OPENAI_API_KEY")
if len(mykey) == 0:
    print("OPENAI_API_KEY env var not found")
    sys.exit(1)
client = OpenAI(api_key=mykey)


def read_jsonl_file(filename):
    with open(filename, 'r') as file:
        return [json.loads(line) for line in file]

def write_jsonl_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(json.dumps(item) + '\n')

def get_embeddings(data):
    for item in data:
        response = client.embeddings.create(input=item['text'], model="text-embedding-3-small")
        item['embedding'] = response.data[0].embedding
    return data

def annotate_with_gpt4(data):
    for item in data:
        prompt = f"{annotation_prompt} \n\"\"\"{item['text']}\"\"\""
        response = client.completions.create(model="gpt-3.5-turbo", prompt=prompt)  # gpt-3.5-turbo
        item['annotate'] = response.choices[0].text.strip()
    return data

def main():
    if len(sys.argv) != 2:
        print("Usage: python annotate.py <filename.jsonl>  # which will write another file")
        sys.exit(1)
    
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print("File does not exist.")
        sys.exit(1)
    
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

