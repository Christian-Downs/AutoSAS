import json
import os
import shutil

def renameOutputFolder (outputName, i) :
    if (os.path.exists("output" + str(i))) :
        renameOutputFolder(outputName, i + 1)
    os.rename(outputName, "output" + str(i))

def safeOpen (path, openType) :
    os.makedirs(os.path.dirname(path), exist_ok = True)
    return open(path, openType)

def writeFile(filepath, fileContent) :
    with safeOpen(filepath, 'w') as file:
        file.write(fileContent)

# takes the directory dir which is the key and json which contains info about items in the dir which is the value
def recursiveWriteFile(dir, json) :
    for fileOrDir in json :
        value = json[fileOrDir]
        if (type(value) is str) :
            writeFile("output/" + dir + "/" + fileOrDir, value)
        else :
            recursiveWriteFile(dir + "/" + fileOrDir, value)

def jsonToProject (nameAndContent): 
    try :
        if (any(os.scandir("output"))) :
            renameOutputFolder("output", 1) # rename output folder to save previous websites, also "deletes" the output folder
    except Exception as e:
        pass


    nameAndContentObject = json.loads(nameAndContent)
    for fileOrDir in nameAndContentObject :
        value = nameAndContentObject[fileOrDir]
        if (type(value) is str) :
            writeFile("output/" + fileOrDir, value)
        else :
            recursiveWriteFile(fileOrDir, value)

# key is filename or the folder name
# value is file contents if it is a string
# value is a dictionary if the key is a folder name

def jsonFromResponse (response) :
    jsonBegin = False
    jsonEnd = True

    json = ""
    for char in response :
        if char == "}" :
            jsonEnd = True
        
        if jsonBegin == True and jsonEnd == False :
            json += char

        if char == "{" :
            jsonBegin = True
            jsonEnd = False
    
    return json

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

jsonToProject(" {\"newFolder/file1\" : \"file1 contents\" , \"file2\" : \"file2 contents\"} ")

print(jsonFromResponse(" {\"newFolder\\file1\" : \"file1 {} contents\" , \"file2\" : \"file2 contents\"} "))


jsonToProject("{\"folder1/folder2/folder3/file1\" : \"file1 content\", \"folder1/folder1/file2\": \"file2 contents\", \"folder1/folder1/file3\" : \"file contents\"}")

# test cases
# subfiles of subfiles
# multiple files in the same directory
# 