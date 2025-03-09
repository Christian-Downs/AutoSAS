import json
import re


def old_convert_text_to_json(input_text: str) -> dict:
     # method uses regex to match certain patterns in output
    result = {}
    
    # Match the file structure header
    file_structure_match = re.search(r'File Structure\s*([\s\S]+?)\s*main.py', input_text)
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

    return json_output

def convert_text_to_json(input_text: str) -> dict:
    lines = input_text.splitlines(keepends=True)
    insideCode = False

    jsonString = "{"

    filepath = ""
    for line in lines :
        if (line.strip() == "```python") :
            insideCode = True
            jsonString += "\"" + filepath + "\"" + ":\""
            continue
        if (line.strip() == "```html") :
            insideCode = True
            jsonString += "\"" + filepath + "\"" + ":\""
            continue
        if (line.strip() == "```css") :
            insideCode = True
            jsonString += "\"" + filepath + "\"" + ":\""
            continue
        if (line.strip() == "```markdown") :
            insideCode = True
            jsonString += "\"" + filepath + "\"" + ":\""
            continue


        splitLines = line.strip().split()
        if not insideCode and len(splitLines) <= 5 and len(splitLines) >= 1:
            if  len(splitLines[0]) != 0 :
                filenameIndex = len(splitLines) - 1
                lastChar = splitLines[filenameIndex][-1]
                while splitLines[filenameIndex] != "`" and splitLines[filenameIndex] != "*" and (lastChar == "`" or lastChar == "*") :
                    print (splitLines[filenameIndex][:-1])
                    splitLines[filenameIndex] = splitLines[filenameIndex][:-1]
                    lastChar = splitLines[filenameIndex][-1]
                firstChar = splitLines[filenameIndex][0]
                while splitLines[filenameIndex] != "`" and splitLines[filenameIndex] != "*" and (firstChar == "`" or firstChar == "*") :
                    splitLines[-1] = splitLines[filenameIndex][1:]
                    firstChar = splitLines[filenameIndex][0]
                filepath = splitLines[filenameIndex]
            
        if(insideCode) :
            line = line.replace("\"", "\\\\\\\"")
            jsonString += line

        if insideCode and line.strip() == "```" :
            insideCode = False
            jsonString = jsonString[:-4] 
            jsonString += "\","
    jsonString = jsonString[:-1]
    jsonString += "}"

    return jsonString

def save_json_to_file(json_data: dict, filename: str):
    with open(filename, "w") as f:
        json.dump(json_data, f, indent=4)

