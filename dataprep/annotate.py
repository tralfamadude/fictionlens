"""
Requires env to have var OPENAI_API_KEY

"""

import json
from openai import OpenAI

import os
import sys

annotation_prompt="""
In the text in triple quotes below, determine the sentiment as -1,0,1 for bad, neutral, good. Identify the names of persons. Format these into a JSON with the keys "sentiment" and "entities". If there are no name or persons or places, "entities" key should have and empty list as value. Only give JSON as the response. 
"""

annotation_prompt="""
Create a JSON from the user text, determine the sentiment as -1,0,1 for bad, neutral, good and use the key "sentiment". Identify the proper names of persons and put in a list of "persons". Identify names of places and put in a list of "places". Use empty lists if nothing is found. Only give JSON as the response. 
"""


# Set up OpenAI key
mykey = os.getenv("OPENAI_API_KEY")
if len(mykey) == 0:
    print("OPENAI_API_KEY env var not found")
    sys.exit(1)
client = OpenAI(api_key=mykey)

# enrichment_llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1, max_tokens=750)


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
        #prompt = f"{annotation_prompt} \n\"\"\"{item['text']}\"\"\""
        # response = client.chat.completions.create(model="gpt-4", messages=[prompt])  # gpt-3.5-turbo
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",   # gpt-4
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": annotation_prompt
                },
                {
                    "role": "user",
                    "content": item['text']
                }
            ]
        )
        annotate = response.choices[0].message.content
        item['annotation'] = annotate
        print(f"RESPONSE={annotate} FROM  {item['text']}")
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

