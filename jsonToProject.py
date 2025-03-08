import json
def jsonToProject (nameAndContent): 
    nameAndContentObject = json.loads(nameAndContent)
    for filename in nameAndContentObject :
        with open(filename, 'w') as file:
            file.write(nameAndContentObject[filename])

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

jsonToProject(" {\"file1\" : \"file1 contents\" , \"file2\" : \"file2 contents\"} ")

print(jsonFromResponse(" {\"file1\" : \"file1 {} contents\" , \"file2\" : \"file2 contents\"} "))