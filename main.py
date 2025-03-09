from flask import Flask, render_template, request
from aiTester import caller
from fileNameParse import convert_text_to_json
from jsonToProject import jsonToProject
import json

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('my-form.html')

def jsonFromResponse (response) :
    openBraceCount = 0

    json = ""
    for char in response :
        if char == "{" :
            openBraceCount += 1
        
        if openBraceCount > 0:
            json += char

        if char == "}" :
            openBraceCount -= 1
    
    return json

def templateJsonToPathJson (badJson) :
    badDict = json.loads(badJson)
    keys = list(badDict.keys())
    fileTemplate = "\"" + badDict[keys[0]] + "\""

    fileJson = json.loads(fileTemplate)
    fileList = list(fileJson.keys())    

{'employee_app': {'': None},
 '│': None,
 '├── main.py': None,
 '├── templates': {'': None}, 
 '│   ├── index.html': None,
 '│   └── employee_list.html': None,
 '└── README.md': None
}
    

@app.route('/', methods=['POST'])
def my_form_post():
    # Example Usage:
    text = request.form['text']

    caller(text)
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        file_content = file.read()
        file.close()
    with open("Output.json", "w") as file:
        json_data = convert_text_to_json(file_content)
        json_data = templateJsonToPathJson(json_data)
        file.write(str(json_data))
    jsonToProject(str(json_data))

    return "PROCESSED"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
