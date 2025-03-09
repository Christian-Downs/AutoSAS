import os
import json
import uuid
import logging

def create_files_from_json(json_data, root_dir):
    """
    Creates files and directories based on the provided JSON data.
    The JSON data should be a dictionary where keys are file paths and values are file contents.
    
    Args:
        json_data (dict): A dictionary where keys are file paths and values are file contents.
        root_dir (str): The root directory where the files will be created.
        
    Returns:
        None
    """
    for file_path, file_content in json_data.items():
        abs_file_path = root_dir + "/" + file_path
        # Create the directory if it doesn't exist
        directory = os.path.dirname(abs_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write content to the file
        with open(abs_file_path, 'w', encoding='utf-8') as file:
            file.write(file_content)

# Expects chat output containing JSON to be in the following format:
# leading text
# ```json
# {
#   "file1.txt": "Content of file 1"
# }
# ```
# trailing text
def chat_output_to_json(chat_output):
    """
    Converts the chat output from ChatGPT into a JSON dictionary.
    
    Args:
        chat_output (str): The output from ChatGPT containing JSON data.
        
    Returns:
        dict: A dictionary containing the JSON data."""
    # Crop off all text before "```json"
    json_start = chat_output.find("```json")
    # Crop off all text after last occurrence of "```"
    json_end = chat_output.rfind("```")
    # Extract the JSON string
    json_string = chat_output[json_start + len("```json"):json_end].strip()

    try:
        # Convert the JSON string into a dictionary
        json_data = json.loads(json_string)
        return json_data
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}. ChatGPT output malformed.")
        return None

if __name__ == "__main__":
    with open('example-input.txt', 'r', encoding='utf-8') as file:
        file_content = file.read()

    random_uuid = uuid.uuid4()

    json_data = chat_output_to_json(file_content)

    create_files_from_json(json_data, "output" + str(random_uuid))
