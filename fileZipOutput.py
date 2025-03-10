import shutil
from flask import Flask, send_file
import requests
from configparser import ConfigParser

# read config file with 'General' section
config = ConfigParser()
config.read('config.ini')

port = config.get('General', 'port', fallback='5000')

#zips file and returns zipped file to user
#folder_to_zip must be called before send_to_user
toZipName = "UserProject.zip"
def folder_to_zip(foldername):
    shutil.make_archive(toZipName.replace('.zip', ''), 'zip', foldername)

# @app.route('/download_zip')
def send_to_user():
    upload = toZipName
    # Send a POST request to the Flask server that the zip file is ready
    # Flask server URL (update if hosted elsewhere)
    url = f"http://127.0.0.1:{port}/set_logging"

    # Log message to append
    new_message = "Zip file is ready to be downloaded!"

    # Send POST request
    response = requests.post(url, json={"message": new_message})

    return send_file(upload, download_name=toZipName, as_attachment=True)