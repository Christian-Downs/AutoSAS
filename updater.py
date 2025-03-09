from openai_test import tester
# Takes in the error from the code and pulls out the file
def pullFile(error:str)->str:
    words = error.split(" ")
    file = ""
    i = 0
    while(i<len(words)):
        print(words[i])
        if words[i] == "line":
            file = words[i-1]
            if "\n" in file:
                file = file.split("\n")[-1]
            file = file.rstrip(''','"''')
            file = "output" + file
            return file

        i+=1
    return file

def file_updater(chat:str, fileLocation:str):
    
    start_i = chat.find("```python")+9
    end_i = chat.rfind("```")
    updated_text = chat[start_i: end_i]

    with open(fileLocation, "w") as file:
        file.write(updated_text)
    

def updater(error:str): 
    file = pullFile(error)
    file_updater(tester(file, error), file)


