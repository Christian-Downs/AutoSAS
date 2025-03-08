import json
import os

def safeOpen (path, openType) :
    os.makedirs(os.path.dirname(path), exist_ok = True)
    return open(path, openType)

def jsonToProject (nameAndContent): 
    nameAndContentObject = json.loads(nameAndContent)
    for filepath in nameAndContentObject :
        with safeOpen("output/" + filepath, 'w') as file:
            file.write(nameAndContentObject[filepath])

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