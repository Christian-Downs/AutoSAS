import json
import re


def convert_text_to_json(input_text: str) -> dict:
    result = {"file_structure": {}}

    # Extract the file structure
    file_structure_match = re.search(r'### File Structure\s*```([\s\S]+?)```', input_text)
    if file_structure_match:
        file_structure_raw = file_structure_match.group(1).strip()
        file_hierarchy = {}


        for line in file_structure_raw.split("\n"):
            line = line.strip().replace("│", "").replace("├──", "").replace("└──", "").strip()
            if not line:
                continue

            parts = line.split("/")
            current_level = file_hierarchy
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # Last part is a file
                    current_level[part] = None  # Use None to indicate empty files
                else:  # Create folder if it doesn't exist
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]

        result["file_structure"] = file_hierarchy

    # Function to navigate and insert content into the correct folder
    def insert_into_structure(path: str, content: str):
        parts = path.split("/")
        current_level = result["file_structure"]
        for i, part in enumerate(parts):
            if part not in current_level:
                current_level[part] = {} if i < len(parts) - 1 else content
            current_level = current_level[part] if isinstance(current_level[part], dict) else current_level

    # Extract all code blocks
    code_blocks = re.findall(r'### `([^`]+)`\n```[a-zA-Z0-9]+\n([\s\S]+?)```', input_text)
    for file_path, file_content in code_blocks:
        insert_into_structure(file_path, file_content.strip())

    return result


def save_json_to_file(json_data: dict, filename: str):
    with open(filename, "w") as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_text = file.read()

    json_output = convert_text_to_json(input_text)
    save_json_to_file(json_output, "Output.json")

    print("JSON structure saved to Output.json")