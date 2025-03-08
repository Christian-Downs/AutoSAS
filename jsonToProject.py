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
    record = False

    json = ""
    for char in response :
        if char == "{" :
            record = True
        
        if record == True:
            json += char

        if char == "}" :
            record = False
    
    return json

jsonToProject(" {\"file1\" : \"file1 contents\" , \"file2\" : \"file2 contents\"} ")

print(jsonFromResponse(" {\"file1\" : \"file1 contents\" , \"file2\" : \"file2 contents\"} "))