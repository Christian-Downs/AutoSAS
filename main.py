from flask import Flask, render_template, jsonify, request

from aiTester import caller
from fileNameParse import convert_text_to_json
from jsonToProject import jsonToProject
import fileZipOutput
from test_code import tester
import json
import shutil
import os
from werkzeug.serving import WSGIRequestHandler

from configparser import ConfigParser

# read config file with 'General' section
config = ConfigParser()
config.read('config.ini')

port = config.get('General', 'port', fallback='5000')

#Render webpage
app = Flask(__name__)

WSGIRequestHandler.timeout = 600  # 10 minutes

# Clear the log file on server restart
if os.path.exists("generation.log"):
    open("generation.log", "w").close()  # Open in "w" mode to overwrite with an empty file

@app.route('/')
def my_form():
    return render_template('main.html')

#Send user input and execute code
@app.route('/', methods=['POST'])
def my_form_post():
    output_folder = 'output'
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    # Example Usage:
    text = request.form.get('text')
    print(request)

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
    
@app.route('/set_logging', methods=['POST'])
def set_log():
    data = request.get_json()
    if 'message' in data:
        with open("generation.log", "a") as f:  # Append mode
            f.write(data['message'] + "\n")  # Append a newline for separation
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/update_logging')
def get_log():
    try:
        with open("generation.log", "r") as f:
            message = f.read()
    except FileNotFoundError:
        message = "No log available."
    return jsonify({"message": message})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=int(port))
