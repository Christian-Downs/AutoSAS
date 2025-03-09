import json
import os
import shutil

""" def renameOutputFolder (outputName, i) :
    if (os.path.exists("output" + str(i))) :
        renameOutputFolder(outputName, i + 1)
    os.rename(outputName, "output" + str(i))

def safeOpen (path, openType) :
    os.makedirs(os.path.dirname(path), exist_ok = True)
    return open(path, openType)

def jsonToProject (nameAndContent): 
    try :
        if (any(os.scandir("output"))) :
            renameOutputFolder("output", 1) # rename output folder to save previous websites, also "deletes" the output folder
    except Exception as e:
        pass
    nameAndContentObject = json.loads(nameAndContent)
    for filepath in nameAndContentObject :
        with safeOpen("output/" + filepath, 'w') as file:
            file.write(str(nameAndContentObject[filepath])) """

    

def safeOpen (path, openType) :
    os.makedirs(os.path.dirname(path), exist_ok = True)
    return open(path, openType)

def jsonToProject (nameAndContent): 
    nameAndContentObject = json.loads(nameAndContent)
    for filepath in nameAndContentObject :
        with safeOpen("output/" + filepath, 'w') as file:
            file.write(str(nameAndContentObject[filepath]))


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

# jsonToProject(" {\"newFolder/file1\" : \"file1 contents\" , \"file2\" : \"file2 contents\"} ")

print(jsonFromResponse(" {\"newFolder\\file1\" : \"file1 {} contents\" , \"file2\" : \"file2 contents\"} "))


jsonToProject("{\"folder1/folder2/folder3/file1\" : \"file1 content\", \"folder1/folder1/file2\": \"file2 contents\", \"folder1/folder1/file3\" : \"file contents\"}")

# test cases
# subfiles of subfiles
# multiple files in the same directory
# 
