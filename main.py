from flask import Flask, render_template, request
from aiTester import caller
from fileNameParse import convert_text_to_json
from jsonToProject import jsonToProject
import fileZipOutput
from test_code import tester
import json

#Render webpage
app = Flask(__name__)



@app.route('/')
def my_form():
    return render_template('my-form.html')

#Send user input and execute code
@app.route('/', methods=['POST'])
def my_form_post():
    # Example Usage:
    text = request.form['text']

    #Send ChatGPT user prompt and store output input.txt
    caller(text)
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
            file_content = file.read()
            file.close()

    #conver input.txt to .json file
    with open("Output.json", "w") as file:
        json_data = convert_text_to_json(file_content)
        file.write(json_data)

    #convert .json to files
    jsonToProject(str(json_data))
    
    tester()


    #convert files to zip and display back to user
    fileZipOutput.folder_to_zip("output")
    return fileZipOutput.send_to_user()
    

if __name__ == '__main__':
    app.run(debug=True)
