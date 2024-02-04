import json

def read_jsonl_file(file_path):
    """
    Reads a JSONL (JSON Lines) file and returns a list of dictionaries.

    Args:
    - file_path (str): The path to the JSONL file to read.

    Returns:
    - list[dict]: A list of dictionaries, each representing a JSON object from the file.
    """
    data_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data_list.append(json.loads(line))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return data_list


def filter_dlist_keys(dlist, retain_keys):
    """
    Filters each dictionary in a list to retain only specified keys.

    Args:
    - dlist (list[dict]): The list of dictionaries to filter.
    - retain_keys (list[str]): The keys to retain in each dictionary.

    Returns:
    - list[dict]: A list of dictionaries with only the retained keys.
    """
    # Create a new list with dictionaries that only contain the retained keys
    filtered_list = [{key: d[key] for key in d if key in retain_keys} for d in dlist]
    return filtered_list


def convert_string_to_dict_in_list(dlist, key_to_convert):
    """
    Converts a string value of a specified key in each dictionary of a list to a dictionary.

    Args:
    - dlist (list[dict]): The list of dictionaries to process.
    - key_to_convert (str): The key whose string value needs to be converted to a dictionary.

    Returns:
    - list[dict]: A list of dictionaries with the specified key's value converted to a dictionary.
    """
    modified_list = []
    for d in dlist:
        # Copy the original dictionary to avoid modifying the input directly
        new_dict = d.copy()
        if key_to_convert in new_dict and isinstance(new_dict[key_to_convert], str):
            try:
                # Attempt to parse the string to a dict
                new_dict[key_to_convert] = json.loads(new_dict[key_to_convert])
            except json.JSONDecodeError:
                # If parsing fails, leave the value as is or handle the error as needed
                pass
        modified_list.append(new_dict)
    return modified_list


def get_paragraphs_with_embedding(filename):
    paras = read_jsonl_file(filename)
    paras = convert_string_to_dict_in_list(paras, 'annotation')
    return paras


def get_paragraphs_without_embedding(filename):
    paras = read_jsonl_file(filename)
    paras = convert_string_to_dict_in_list(paras, 'annotation')
    paras = filter_dlist_keys(paras, ["id", "text", "annotation"])
    return paras


def get_paragraphs_without_embedding_text(filename):
    paras = read_jsonl_file(filename)
    paras = convert_string_to_dict_in_list(paras, 'annotation')
    paras = filter_dlist_keys(paras, ["id", "annotation"])
    return paras

