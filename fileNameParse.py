import json
import re


#This function converts an AI response into corresponding json file
def convert_text_to_json(input_text: str) -> str:

    # method uses regex to match certain patterns in output
    result = {}
    
    # Match the file structure header
    file_structure_match = re.search(r'File Structure\s*([\s\S]+?)\s*```', input_text)

    if file_structure_match:
        file_structure_raw = file_structure_match.group(1).strip()
        file_structure = {}
        
        # Process file structure
        for line in file_structure_raw.split('\n'):
            line = line.strip()
            if line:
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    file_structure[parts[0]] = parts[1]
        result['file_structure'] = file_structure
    
    # Extract Python script content
    python_code_match = re.search(r'### main.py\n```python\n([\s\S]+?)```', input_text)
    if python_code_match:
        result['main.py'] = python_code_match.group(1).strip()
    
    # Extract HTML content
    templates = {}
    html_files = re.findall(r'### templates/([a-zA-Z0-9_\-]+.html)\n```html\n([\s\S]+?)```', input_text)
    for file_name, file_content in html_files:
        templates[file_name] = file_content.strip()
    if templates:
        result['templates'] = templates
    
    # Extract static file content
    static_files = re.findall(r'### static/([a-zA-Z0-9_\-]+.css)\n```css\n([\s\S]+?)```', input_text)
    static = {}
    for file_name, file_content in static_files:
        static[file_name] = file_content.strip()
    if static:
        result['static'] = static
    
    # Extract README content
    readme_match = re.search(r'### README.md\n```markdown\n([\s\S]+?)```', input_text)
    if readme_match:
        result['README.md'] = readme_match.group(1).strip()

    # Convert the result dictionary to JSON string
    json_output = json.dumps(result, indent=4)
    save_json_to_file(str(json_output), "Output.json")
    return json_output

def save_json_to_file(json_data: str, filename: str):
    with open(filename, 'w') as f:
        f.write(json_data)
        f.close()




if __name__ == '__main__':
    convert_text_to_json(open('input.txt', 'r').read())