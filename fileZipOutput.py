import shutil
from flask import Flask, send_file

#zips file and returns zipped file to user
#folder_to_zip must be called before send_to_user
toZipName = "UserProject.zip"
def folder_to_zip(foldername):
    shutil.make_archive(toZipName.replace('.zip', ''), 'zip', foldername)

@app.route('/download_zip')
def send_to_user():
    upload = toZipName
    return send_file(upload, download_name=toZipName, as_attachment=True)