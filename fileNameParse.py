import json
import re


def convert_text_to_json(input_text: str) -> dict:
    lines = input_text.split("\n")
    insideCode = False

    jsonString = "{"

    filepath = ""
    for line in lines :
        if (line == "```python") :
            insideCode = True
            jsonString += "\"" + filepath + "\"" + ":\""
        if (line == "```html") :
            insideCode = True
            jsonString += "\"" + filepath + "\"" + ":\""
        if (line == "```markdown") :
            insideCode = True
            jsonString += "\"" + filepath + "\"" + ":\""

        if r"*`*`" in line :
            filepath = r"`*`"
            filepath = filepath.replace("`",'"')
        
        if(insideCode) :
            jsonString += line

        if insideCode and line == "```" :
            insideCode = False
            jsonString += "\","
    jsonString = jsonString[:-1]
    jsonString = jsonString[:-1]
    jsonString += "}"

    return jsonString

def save_json_to_file(json_data: dict, filename: str):
    with open(filename, "w") as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_text = file.read()

    json_output = convert_text_to_json(input_text)
    save_json_to_file(json_output, "Output.json")

    print("JSON structure saved to Output.json")