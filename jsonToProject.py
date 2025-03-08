import json
def jsonToProject (nameAndContent): 
    nameAndContentObject = json.loads(nameAndContent)
    for filename in nameAndContentObject :
        with open(filename, 'w') as file:
            file.write(nameAndContentObject[filename])


jsonToProject(" {\"file1\" : \"file1 contents\" , \"file2\" : \"file2 contents\"} ")
